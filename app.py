from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem
import re
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from API.User_autorization import DB_Api_Autorization
from Gui_win.Autorization import Ui_Autorization_win
from Gui_win.Registration_win import Ui_Registration_win
from main import client_interface
from main import admin_interface
from main import master_interface
import sys



class AutorizationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Autorization_win()
        self.ui.setupUi(self)

        self.DB = DB_Api_Autorization()

        self.ui.pushButton_autoriz.clicked.connect(self.autor_in)
        self.ui.pushButton_registration_f_autor.clicked.connect(self.open_registration_window)

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.close()

    def autor_in(self):
        _login = self.ui.lineEdit_login_autoriz.text().strip()
        _password = self.ui.lineEdit_password_autoriz.text().strip()

        try:
            role = self.DB.authorization(_login, _password)

            if role:
                print(f"Авторизация прошла успешно. Роль: {role}")
                # Открытие главного окна в зависимости от роли
                if role == 'Администратор':
                    self.admin_interface = admin_interface()
                    self.admin_interface.show()
                elif role == 'Клиент':
                    self.client_interface = client_interface()
                    self.client_interface.show()
                elif role == 'Мастер':
                    self.master_interface = master_interface()
                    self.master_interface.show()
                self.close()  # Закрываем окно авторизации
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

        except Exception as e:
            # Обработка исключений
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")


class RegistrationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Registration_win()
        self.ui.setupUi(self)

        self.DB = DB_Api_Autorization()
        self.ui.comboBox_registr.addItem("Администратор")
        self.ui.comboBox_registr.addItem("Клиент")
        self.ui.comboBox_registr.addItem("Мастер")
        self.ui.pushButton_registr_user.clicked.connect(self.register_user)
        self.ui.pushButton_registration_f_autor.clicked.connect(self.open_autoriz_win)

    def open_autoriz_win(self):
        self.autorization_window = AutorizationWindow()
        self.autorization_window.show()
        self.close()

    def register_user(self):
        """Регистрирует нового пользователя в системе."""
        role_log = self.ui.comboBox_registr.currentText()
        login = self.ui.lineEdit_login_registr.text().strip()
        password = self.ui.lineEdit_password_registr.text().strip()
        phone = self.ui.lineEdit_telephone_registr.text().strip()
        fio = self.ui.lineEdit_fio_registr.text().strip()



        # Проверка заполнения всех полей
        if not role_log or not login or not password or not phone or not fio:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверка уникальности логина
        if not self.is_unique_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин уже занят. Выберите другой.")
            return

        # Сохранение пользователя в базе данных
        if self.DB.register_new_user(fio, phone, role_log, login, password):
            QMessageBox.information(self, "Успешно", "Регистрация прошла успешно.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрироваться. Повторите попытку.")

    def is_unique_login(self, login):
        """Проверяет уникальность логина в базе данных."""
        return self.DB.check_login_unique(login)  # Метод API для проверки уникальности логина





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    icon = QtGui.QIcon("D:/Py_Projects/OOO_Polus-main-main/В2_Ресурсы/resourse.ico")
    app.setWindowIcon(icon)
    start_app = AutorizationWindow()
    start_app.show()
    sys.exit(app.exec_())

