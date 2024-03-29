from logs.my_logging import log
from http_.request import Request, ParseErorr
from services.todo_service import TodoService
from services.user_service import UserService
from utils.my_errors import MyErrors as err
from services.session_service import SessionService


class Post:
    def register(self, uid, user_id):
        try:
            user_data = Request.parse(self, register_schema)
            UserService.register_user(user_data)
            Request.respond(self, 200, f"'{user_data['login']}' registered.")
            log.info(f"New user: {user_data['login']} registered.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.EmailValidationError:
            Request.respond(
                self, 400, "Error, email is not valid!")
        except err.UserAlreadyExistsError:
            Request.respond(
                self, 400, "Error, user with the requested data already exists!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")

    def login(self, uid, user_id):
        try:
            user_data = Request.parse(self, login_schema)
            user_id = UserService.login_user(user_data)
            # use session service to create new session in redis_db
            uid = SessionService.new_session(user_id)

            Request.respond(
                self, 200, "User has been authorized.", uid, user_id)
            log.info("User has been authorized.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except (err.UserNotFounError, err.IncorrectPasswordError):
            Request.respond(
                self, 400, "Error, incorrect login or password entered!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.RedisConnectionError:
            Request.respond(
                self, 503, "Internal error. Try again later.")

    def new(self, uid, user_id):
        '''Method for creating a new todo'''
        # check authorization
        if SessionService.check_redis_session(user_id, uid) == False:
            Request.respond(self, 401, "Auth error.")
            return
        try:
            new_todo = Request.parse(self, new_todo_schema)
            TodoService.create_todo(new_todo, user_id)
            Request.respond(self, 200, "New todo has been created.")
            log.info("New todo has been created.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.RedisConnectionError:
            Request.respond(
                self, 503, "Internal error. Try again later.")

    def logout(self, uid, user_id):
        # check authorization
        if SessionService.check_redis_session(user_id, uid) == False:
            Request.respond(self, 401, "Auth error.")
            return
        try:
            SessionService.end_session(user_id)
            Request.respond(self, 200, "User logged out.")
            log.info(
                f"Session '{uid}' ended. User has logged out.")

        except err.RedisConnectionError:
            Request.respond(
                self, 503, "Internal error. Try again later.")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")


# Templates for Request.parse
# Register template
register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "login": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["name", "login", "password", "email"],
    "additionalProperties": False
}

# Login template
login_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["login", "password"],
    "additionalProperties": False
}

# Template for new todo
new_todo_schema = {
    "type": "object",
    "properties": {
        "task": {"type": "string"}
    },
    "required": ["task"],
    "additionalProperties": False
}
