# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\QtDesign\masters_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_masters_info_win(object):
    def setupUi(self, Dialog_masters_info_win):
        Dialog_masters_info_win.setObjectName("Dialog_masters_info_win")
        Dialog_masters_info_win.resize(708, 555)
        self.tableView_show_masters = QtWidgets.QTableView(Dialog_masters_info_win)
        self.tableView_show_masters.setGeometry(QtCore.QRect(9, 9, 691, 531))
        self.tableView_show_masters.setObjectName("tableView_show_masters")

        self.retranslateUi(Dialog_masters_info_win)
        QtCore.QMetaObject.connectSlotsByName(Dialog_masters_info_win)

    def retranslateUi(self, Dialog_masters_info_win):
        _translate = QtCore.QCoreApplication.translate
        Dialog_masters_info_win.setWindowTitle(_translate("Dialog_masters_info_win", "Список мастеров"))
