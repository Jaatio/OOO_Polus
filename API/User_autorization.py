import pymysql.cursors
import pymysql
import sys
from decimal import Decimal

class DB_Api_Autorization:

    def __init__(self):
        # Создание соединения с базой данных
        try:
            self.connection = pymysql.connect(host='localhost',
                                              user='root',
                                              password='1234',
                                              database='OOO_Polus',
                                              cursorclass = pymysql.cursors.DictCursor)

            print("Соединение с базой данных установлено")
        except pymysql.MySQLError as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            sys.exit()

    def authorization(self, login, password):
        try:
            with self.connection.cursor() as cursor:
                # Выполнение SQL-запроса для проверки логина и пароля
                sql_query = "SELECT role_log FROM user_info WHERE login=%s AND password=%s"
                cursor.execute(sql_query, (login, password))
                result = cursor.fetchone()  # fetchone вернёт результат в виде словаря

                if result:
                    return result['role_log']  # Можно безопасно обращаться через строковые индексы
                else:
                    return None
        except pymysql.MySQLError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def register_new_user(self, fio, phone, role_log, login, password):
        """Регистрирует нового пользователя в базе данных."""
        try:
            query = """
                INSERT INTO user_info (fio, phone, role_log, login, password)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (fio, phone, role_log, login, password))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            return False

    def check_login_unique(self, login):
        """Проверяет уникальность логина в базе данных."""
        query = "SELECT COUNT(*) AS count FROM user_info WHERE login = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (login,))
        result = cursor.fetchone()  # fetchone() возвращает словарь, если используется DictCursor

        # Проверяем, что результат существует и количество пользователей с таким логином равно 0
        if result and result.get('count', 0) == 0:
            return True  # Логин уникален
        return False  # Логин уже существует
DB = DB_Api_Autorization()
