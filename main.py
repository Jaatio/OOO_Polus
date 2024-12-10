from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem
import re
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Gui_win.client_main import Ui_Dialog_client_win
from Gui_win.masters_info import Ui_Dialog_masters_info_win
from Gui_win.admin_win import Ui_Dialog_admin_win
from Gui_win.master_win import Ui_Dialog_master_win
from Gui_win.components_inspection import Ui_Dialog_components_inspection
from Gui_win.master_messages import Ui_Dialog_messages_admin
from Gui_win.orders_history import Ui_Dialog_orders_history
from Gui_win.master_order_work import Ui_Dialog_order_work


from API.client_api import DB_Client_api
from API.client_api import DB_admin_api
from API.client_api import DB_master_api

import sys

class client_interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_client_win()
        self.ui.setupUi(self)
        self.DB = DB_Client_api()
        self.ui.comboBox_org_tech_type.addItem("Компьютер")
        self.ui.comboBox_org_tech_type.addItem("Ноутбук")
        self.ui.comboBox_org_tech_type.addItem("Принтер")
        self.ui.pushButton_push_application.clicked.connect(self.Push_app)
        self.ui.pushButton_exit_3.clicked.connect(self.Exit_but)



    def Exit_but(self):
        from app import AutorizationWindow
        self.AW = AutorizationWindow()
        self.AW.show()
        self.close()

    def Push_app(self):
        org_tech_type = self.ui.comboBox_org_tech_type.currentText()
        problem_description = self.ui.textEdit_problem_description.toPlainText()
        org_tech_model = self.ui.lineEdit_model_type.text().strip()
        client_fio = self.ui.lineEdit_client_fio.text().strip()


        # Проверка заполнения всех полей
        if not org_tech_type or not problem_description or not org_tech_model or not client_fio:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return
        print(f"Debug: {org_tech_type}, {org_tech_model}, {problem_description}, {client_fio}")

        # Сохранение пользователя в базе данных
        if self.DB.add_application(org_tech_type, org_tech_model, problem_description, client_fio):
            QMessageBox.information(self, "Успех", "Заявка успешно отправлена.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось отправить заявку. Повторите попытку.")


class admin_interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_admin_win()
        self.ui.setupUi(self)
        self.DB = DB_admin_api()

        # Разрешаем редактирование таблицы
        self.ui.tableWidget_app_output.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # Загрузка данных при старте
        self.load_table_data("application")  # Замените "application" на имя вашей таблицы

        # Обработчик изменений
        self.ui.tableWidget_app_output.itemChanged.connect(self.update_database)

        self.ui.pushButton_show_masters.clicked.connect(self.open_masters_win)
        self.ui.pushButton_show_masters_messages.clicked.connect(self.open_master_messages)
        self.ui.pushButton_orders_history.clicked.connect(self.open_orders_history_win)
        self.ui.pushButton_exit.clicked.connect(self.Exit_but)

    def Exit_but(self):
        from app import AutorizationWindow
        self.AW = AutorizationWindow()
        self.AW.show()
        self.close()


    def open_masters_win(self):
        self.masters_win = masters_info()
        self.masters_win.show()

    def open_orders_history_win(self):
        self.o_history_win = orders_history()
        self.o_history_win.show()


    def open_master_messages(self):
       self.master_message = masters_messages()
       self.master_message.show()



    def load_table_data(self, application):
        """
        Загружает данные из базы данных и отображает их в tableWidget_app_output.
        """
        column_names, rows = self.DB.fetch_data(application)

        if not column_names or not rows:
            self.ui.tableWidget_app_output.setRowCount(0)
            self.ui.tableWidget_app_output.setColumnCount(0)
            return

        # Настройка таблицы
        self.ui.tableWidget_app_output.setColumnCount(len(column_names))
        self.ui.tableWidget_app_output.setHorizontalHeaderLabels(column_names)
        self.ui.tableWidget_app_output.setRowCount(len(rows))

        # Заполнение таблицы
        for row_idx, row in enumerate(rows):
            for col_idx, column_name in enumerate(column_names):
                value = str(row[column_name])  # Преобразуем значение в строку
                self.ui.tableWidget_app_output.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def update_database(self, item):
        """
        Обрабатывает изменения данных в таблице и вызывает API для обновления базы данных.
        """
        table_name = "application"  # Имя таблицы в базе данных

        # Получаем данные о редактируемой ячейке
        new_value = item.text()
        row = item.row()
        column = item.column()

        # Название столбца из заголовков
        column_name = self.ui.tableWidget_app_output.horizontalHeaderItem(column).text()

        # Первичный ключ строки (application_id)
        primary_key_column = "application_id"  # Указываем правильное имя столбца
        primary_key_value = self.ui.tableWidget_app_output.item(row,0).text()  # Предполагаем, что application_id в первом столбце

        # Вызов API для обновления записи
        success = self.DB.update_record(table_name, column_name, new_value, primary_key_column, primary_key_value)
        if not success:
            print("Ошибка при обновлении данных в базе.")


class orders_history(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_orders_history()  # Ваш интерфейс, созданный в Qt Designer
        self.ui.setupUi(self)
        self.DB = DB_admin_api()


        self.output_orders("orders_status")

    def output_orders(self, orders_status):

        column_names, rows = self.DB.fetch_data_messages(orders_status)

        if not column_names or not rows:
            self.ui.tableWidge_orders_history.setRowCount(0)
            self.ui.tableWidge_orders_history.setColumnCount(0)
            return

        # Настройка колонок
        self.ui.tableWidge_orders_history.setColumnCount(len(column_names))
        self.ui.tableWidge_orders_history.setHorizontalHeaderLabels(column_names)

        # Настройка строк
        self.ui.tableWidge_orders_history.setRowCount(len(rows))

        # Заполнение таблицы
        for row_idx, row in enumerate(rows):
            for col_idx, column_name in enumerate(column_names):
                item = QTableWidgetItem(str(row[column_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidge_orders_history.setItem(row_idx, col_idx, item)

        # Автоматическое изменение размеров колонок
        self.ui.tableWidge_orders_history.resizeColumnsToContents()

class masters_messages(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_messages_admin()  # Ваш интерфейс, созданный в Qt Designer
        self.ui.setupUi(self)
        self.DB = DB_admin_api()
        self.output_masters_messages("message")


    def output_masters_messages(self, message):

        column_names, rows = self.DB.fetch_data_messages(message)

        if not column_names or not rows:
            self.ui.tableWidget_output_messages.setRowCount(0)
            self.ui.tableWidget_output_messages.setColumnCount(0)
            return

        # Настройка колонок
        self.ui.tableWidget_output_messages.setColumnCount(len(column_names))
        self.ui.tableWidget_output_messages.setHorizontalHeaderLabels(column_names)

        # Настройка строк
        self.ui.tableWidget_output_messages.setRowCount(len(rows))

        # Заполнение таблицы
        for row_idx, row in enumerate(rows):
            for col_idx, column_name in enumerate(column_names):
                item = QTableWidgetItem(str(row[column_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_output_messages.setItem(row_idx, col_idx, item)

        # Автоматическое изменение размеров колонок
        self.ui.tableWidget_output_messages.resizeColumnsToContents()




class masters_info(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_masters_info_win()  # Ваш интерфейс, созданный в Qt Designer
        self.ui.setupUi(self)
        self.DB = DB_admin_api()

        # Загрузка данных в таблицу
        self.load_table_data("master_info")


    def load_table_data(self, table_name):
        """
        Загружает данные из таблицы master_info и отображает их в tableView_show_masters.
        """
        column_names, rows = self.DB.fetch_data_masters(table_name)

        if not column_names or not rows:
            print("Нет данных для отображения.")
            return

        # Создание модели для QTableView
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(column_names)

        # Заполнение модели данными
        for row in rows:
            items = [QStandardItem(str(row[column])) for column in column_names]
            model.appendRow(items)

        # Установка модели в tableView
        self.ui.tableView_show_masters.setModel(model)

class master_interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_master_win()
        self.ui.setupUi(self)
        self.DB = DB_master_api()

        self.ui.pushButton_push_message.clicked.connect(self.Push_message)
        self.ui.pushButton_repairs_watch.clicked.connect(self.open_components_win_inspect)
        self.ui.pushButton_order_work.clicked.connect(self.open_master_order_work)
        self.ui.pushButton_exit_2.clicked.connect(self.Exit_but)
    def Exit_but(self):
        from app import AutorizationWindow
        self.AW = AutorizationWindow()
        self.AW.show()
        self.close()

    def open_master_order_work(self):
        self.o_m_w = masters_orders_work()
        self.o_m_w.show()


    def open_components_win_inspect(self):
        self.components_inspection_ow = components_inspection()
        self.components_inspection_ow.show()


    def Push_message(self):
        order_description = self.ui.textEdit_master_message.toPlainText()

        # Проверка заполнения всех полей
        if not order_description:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Сохранение пользователя в базе данных
        if self.DB.push_message_in_db(order_description):
            QMessageBox.information(self, "Успех", "Заявка успешно отправлена.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось отправить заявку. Повторите попытку.")


class masters_orders_work(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_order_work()  # Your UI setup
        self.ui.setupUi(self)
        self.DB = DB_admin_api()
        self.DB_M = DB_master_api()

        # Load existing orders into comboBox_order_id
        self.load_order_ids()

        self.ui.pushButton_push_info_in.clicked.connect(self.Push_order_info)
        self.load_table_orders("application")


    def load_order_ids(self):
        """
        Load order IDs into comboBox_order_id from the application table.
        """
        column_names, rows = self.DB.fetch_data("application")

        # Assuming the first column is application_id
        if rows:
            for row in rows:
                self.ui.comboBox_order_id.addItem(str(row['application_id']), row['application_id'])

    def Push_order_info(self):
        selected_order_id = self.ui.comboBox_order_id.currentData()  # Get selected ID
        repair_name = self.ui.lineEdit_components_name.text().strip()
        repair_quantity = self.ui.lineEdit_components_quantity.text().strip()

        # Проверка заполнения всех полей
        if not selected_order_id or not repair_name or not repair_quantity:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Сохранение данных в базе данных
        if self.DB_M.add_application_master(selected_order_id, repair_name, repair_quantity):
            QMessageBox.information(self, "Успех", "Заявка успешно обновлена.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить заявку. Повторите попытку.")

    def load_table_orders(self, application):
        """
        Загружает данные из базы данных и отображает их в tableWidget_app_output.
        """
        column_names, rows = self.DB.fetch_data(application)

        if not column_names or not rows:
            self.ui.tableWidget_orders_output.setRowCount(0)
            self.ui.tableWidget_orders_output.setColumnCount(0)
            return

        # Настройка таблицы
        self.ui.tableWidget_orders_output.setColumnCount(len(column_names))
        self.ui.tableWidget_orders_output.setHorizontalHeaderLabels(column_names)
        self.ui.tableWidget_orders_output.setRowCount(len(rows))

        # Заполнение таблицы
        for row_idx, row in enumerate(rows):
            for col_idx, column_name in enumerate(column_names):
                value = str(row[column_name])  # Преобразуем значение в строку
                self.ui.tableWidget_orders_output.setItem(row_idx, col_idx, QTableWidgetItem(value))









class components_inspection(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_components_inspection()
        self.ui.setupUi(self)
        self.DB = DB_master_api()  # Подключение API для работы с базой данных

        # Загрузка данных в tableWidget и comboBox
        self.output_components("components")
        self.populate_components_comboBox()

        # Связываем кнопку с методом
        self.ui.pushButton_repairs_buy.clicked.connect(self.buy_components)

    def output_components(self, table_name):
        """
        Вывод данных из таблицы в tableWidget.
        """
        column_names, rows = self.DB.fetch_data_components(table_name)

        if not column_names or not rows:
            self.ui.tableWidget_repairs_output.setRowCount(0)
            self.ui.tableWidget_repairs_output.setColumnCount(0)
            return

        # Настройка колонок
        self.ui.tableWidget_repairs_output.setColumnCount(len(column_names))
        self.ui.tableWidget_repairs_output.setHorizontalHeaderLabels(column_names)

        # Настройка строк
        self.ui.tableWidget_repairs_output.setRowCount(len(rows))

        # Заполнение таблицы
        for row_idx, row in enumerate(rows):
            for col_idx, column_name in enumerate(column_names):
                item = QTableWidgetItem(str(row[column_name]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_repairs_output.setItem(row_idx, col_idx, item)

        # Автоматическое изменение размеров колонок
        self.ui.tableWidget_repairs_output.resizeColumnsToContents()

    def populate_components_comboBox(self):


        try:
            column_names, rows = self.DB.fetch_data_components("components")
            if rows:
                self.ui.comboBox_output_components.clear()
                for row in rows:
                    self.ui.comboBox_output_components.addItem(row["component_name"])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить компоненты: {e}")

    def buy_components(self):
        """
        Логика добавления нового количества компонентов в базу данных.
        """
        try:
            # Получаем выбранный компонент и количество
            selected_component = self.ui.comboBox_output_components.currentText()
            additional_quantity = self.ui.lineEdit_quantity_insert.text()

            if not additional_quantity.isdigit():
                QMessageBox.warning(self, "Ошибка", "Введите корректное число в поле количества.")
                return

            additional_quantity = int(additional_quantity)

            # Получаем текущее количество компонента
            query = f"SELECT component_quantity FROM components WHERE component_name = %s"
            with self.DB.connection.cursor() as cursor:
                cursor.execute(query, (selected_component,))
                result = cursor.fetchone()

                if not result:
                    QMessageBox.warning(self, "Ошибка", "Компонент не найден.")
                    return

                current_quantity = result["component_quantity"]

                # Обновляем количество в базе данных
                new_quantity = current_quantity + additional_quantity
                update_query = f"UPDATE components SET component_quantity = %s WHERE component_name = %s"
                cursor.execute(update_query, (new_quantity, selected_component))
                self.DB.connection.commit()

                QMessageBox.information(self, "Успех", f"Количество для '{selected_component}' обновлено до {new_quantity}.")

                # Обновляем tableWidget
                self.output_components("components")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить операцию: {e}")





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    icon = QtGui.QIcon("D:/Py_Projects/OOO_Polus-main-main/В2_Ресурсы/resourse.ico")  # Путь к файлу иконки
    app.setWindowIcon(icon)
    start_app = client_interface()
    start_app.show()
    sys.exit(app.exec_())
