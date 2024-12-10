import pymysql.cursors
import pymysql
import sys
from decimal import Decimal
from API.User_autorization import DB_Api_Autorization


class DB_Client_api:

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

    def add_application(self, org_tech_type, org_tech_model, problem_description, client_fio):
        try:
            query = """
                INSERT INTO application (org_tech_type, org_tech_model, problem_description, client_fio, application_status)
                VALUES (%s, %s, %s, %s, %s)
            """
            print(f"SQL Query: {query}")
            print(f"Arguments: {org_tech_type}, {org_tech_model}, {problem_description}, {client_fio}, 'Новая заявка'")
            cursor = self.connection.cursor()
            cursor.execute(query, (org_tech_type, org_tech_model, problem_description, client_fio, 'Новая заявка'))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Ошибка при добавлении заявки: {e}")
            return False


class DB_admin_api:
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

    def fetch_data(self, application):
        """
        Извлекает все данные из указанной таблицы.
        """
        try:
            with self.connection.cursor() as cursor:
                # Получить данные
                cursor.execute(f"SELECT * FROM {application}")
                rows = cursor.fetchall()

                # Получить названия столбцов
                column_names = [desc[0] for desc in cursor.description]
                return column_names, rows
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return [], []

    def update_record(self, table_name, column_name, new_value, primary_key_column, primary_key_value):
        """
        Обновляет запись в таблице базы данных.
        """
        query = f"UPDATE {table_name} SET {column_name} = %s WHERE {primary_key_column} = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (new_value, primary_key_value))
            self.connection.commit()
            print(f"Обновлено: {column_name} = {new_value} для {primary_key_column} = {primary_key_value}")
            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            self.connection.rollback()
            return False

    def fetch_data_masters(self, master_info):
        """
        Извлекает все данные из таблицы master_info.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {master_info}")
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return column_names, rows
        except Exception as e:
            print(f"Ошибка при извлечении данных из {master_info}: {e}")
            return [], []

    def fetch_data_messages(self, message):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {message}")
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return column_names, rows
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return [], []

    def fetch_orders_history(self, orders_status):

        try:
            with self.connection.cursor() as cursor:
                # Получить данные
                cursor.execute(f"SELECT * FROM {orders_status}")
                rows = cursor.fetchall()

                # Получить названия столбцов
                column_names = [desc[0] for desc in cursor.description]
                return column_names, rows
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return [], []
class DB_master_api:
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

    def push_message_in_db(self, order_description):

        try:
            query = """
                        INSERT INTO message (message)
                        VALUES (%s)
                    """
            cursor = self.connection.cursor()
            cursor.execute(query, (order_description))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            return False

    def fetch_data_components(self, components):
        """
        Извлекает все данные из таблицы master_info.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {components}")
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return column_names, rows
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return [], []


    def add_application_master(self,order_id, repair_name, repair_quantity):
        try:
            query = """
                    UPDATE application
                    SET repair_name = %s, repair_quantity = %s
                    WHERE application_id = %s
                """
            cursor = self.connection.cursor()
            cursor.execute(query, (repair_name, repair_quantity, order_id))
            self.connection.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Ошибка при обновлении заявки: {e}")
            return False