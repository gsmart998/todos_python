from logs.my_logging import log
from database.db_main import query


class DbUsers:

    def create_user(user_data: dict) -> None:
        """
        Accepts user_data: dict as input.
        user: ("name", "email", "login", "password")
        """
        ud = user_data
        user = (ud["name"], ud["email"], ud["login"], ud["password"])
        _, error = query("push", create_user_template, user)
        if error != None:
            return error

    def check_user(user_data: dict):
        """
        Recive user_data = dict
        user = (ud["login"], ud["email"])
        If user found - return user tuple.
        Else return None.
        """
        ud = user_data
        user = (ud["login"], ud["email"])
        result, error = query("fetch_one", check_user_template, user)
        if error != None:
            return None, error

        if result != None:
            log.info("'Check_user' User found.")
            return result, None
        else:
            log.info("'Check_user' User not found.")
            return None, None


# Templates:
#
# # Query for user create
create_user_template = """
INSERT INTO
users (name, email, login, password)
VALUES
(%s, %s, %s, %s);
"""


# Query for user search
check_user_template = """
SELECT * FROM users WHERE login = %s OR email = %s;
"""
