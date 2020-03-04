# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/scale_limits_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(343, 262)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.add_limit_button = QtWidgets.QPushButton(Dialog)
        self.add_limit_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.add_limit_button.setFont(font)
        self.add_limit_button.setObjectName("add_limit_button")
        self.horizontalLayout_2.addWidget(self.add_limit_button)
        self.remove_limit_button = QtWidgets.QPushButton(Dialog)
        self.remove_limit_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.remove_limit_button.setFont(font)
        self.remove_limit_button.setObjectName("remove_limit_button")
        self.horizontalLayout_2.addWidget(self.remove_limit_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.limits_table = QtWidgets.QTableWidget(Dialog)
        self.limits_table.setObjectName("limits_table")
        self.limits_table.setColumnCount(3)
        self.limits_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.limits_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.limits_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.limits_table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_3.addWidget(self.limits_table)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.accept_button = QtWidgets.QPushButton(Dialog)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout.addWidget(self.accept_button)
        self.reject_button = QtWidgets.QPushButton(Dialog)
        self.reject_button.setObjectName("reject_button")
        self.horizontalLayout.addWidget(self.reject_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение пределов шкалы"))
        self.add_limit_button.setText(_translate("Dialog", "+"))
        self.remove_limit_button.setText(_translate("Dialog", "-"))
        item = self.limits_table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Предел"))
        item = self.limits_table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Класс\n"
"точности"))
        item = self.limits_table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Тип\n"
"сигнала"))
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.reject_button.setText(_translate("Dialog", "Отмена"))
