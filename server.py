from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from sqlite3 import Error


host = "localhost"
port = 8000


# Подключение к БД
path = "app_sqlite.db"


# Создание подключение к БД
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection(path)


# Функция выполнения SQL запроса
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Запрос на создание таблицы users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  login VARCHAR(20) NOT NULL UNIQUE,
  password VARCHAR(20) NOT NULL
);
"""
execute_query(connection, create_users_table)

'''select = """
SELECT * FROM users;
"""
execute_query(connection, select)'''


# Запрос на создание таблицы tasks
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task VARCHAR(100) NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
execute_query(connection, create_tasks_table)


'''
# Запрос на создание пользователя
create_user = """
INSERT INTO
  users (name, email, login, password)
VALUES
  ('John', 'admin@mail.com', 'admin', 'admin123');
"""
execute_query(connection, create_user)
'''


class ServerHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get request recived!")
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        self.wfile.write(
            bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))

    def do_POST(self):
        # Получение длины тела запроса
        content_length = int(self.headers["Content-Length"])

        # Получение тела запроса
        body = self.rfile.read(content_length)
        body = json.loads(body)  # конвертируем json в словарь

        # ------------------------------------

        # Обработка регистрации
        if self.path == "/register":
            print("Получен запрос /register")

            # Проверка ключей в запросе
            if body.get("name", "login") is not None and body.get("password", "email") is not None:
                print("its ok")
                # do some stuff

            else:
                print("Error, incorrect json file!")

        # Обработка авторизации
        if self.path == "/login":
            print("Получен запрос /login")

        # Обработка выхода
        if self.path == "/logout":
            print("Получен запрос /logout")

         # ------------------------------------

        # Формирование ответа
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # body = str(body)
        # print(body)
        # print(type(body))
        """if body == b"add":
            print("Add a new user")
            print(self.path)  # self.path - path in URL "/add"
        else:
            self.wfile.write(bytes(
                "Недоступная команда!. Список доступных команд: add, remove, edit", "utf-8"))"""
        # response = BytesIO()
        # response.write(b"This is POST request. ")
        # response.write(b"Received: ")
        # response.write(body)


server = HTTPServer((host, port), ServerHTTP)

print("Server now running...")
server.serve_forever()
server.shutdown()
