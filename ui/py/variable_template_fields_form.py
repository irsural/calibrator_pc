# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/variable_template_fields_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 146)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.serial_number_edit = QtWidgets.QLineEdit(Dialog)
        self.serial_number_edit.setObjectName("serial_number_edit")
        self.gridLayout_4.addWidget(self.serial_number_edit, 3, 0, 1, 1)
        self.user_name_edit = QtWidgets.QLineEdit(Dialog)
        self.user_name_edit.setObjectName("user_name_edit")
        self.gridLayout_4.addWidget(self.user_name_edit, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 2, 1, 1, 1)
        self.owner_edit = QtWidgets.QLineEdit(Dialog)
        self.owner_edit.setObjectName("owner_edit")
        self.gridLayout_4.addWidget(self.owner_edit, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)
        self.date_edit = QtWidgets.QDateTimeEdit(Dialog)
        self.date_edit.setReadOnly(False)
        self.date_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date_edit.setAccelerated(False)
        self.date_edit.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.date_edit.setObjectName("date_edit")
        self.gridLayout_4.addWidget(self.date_edit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.accept_button = QtWidgets.QPushButton(Dialog)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_2.addWidget(self.accept_button)
        self.reject_button = QtWidgets.QPushButton(Dialog)
        self.reject_button.setObjectName("reject_button")
        self.horizontalLayout_2.addWidget(self.reject_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Введите необходимые поля"))
        self.label_2.setText(_translate("Dialog", "Организация-владелец"))
        self.label_4.setText(_translate("Dialog", "Дата поверки"))
        self.date_edit.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy"))
        self.label_3.setText(_translate("Dialog", "Заводской номер"))
        self.label.setText(_translate("Dialog", "Поверитель"))
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.reject_button.setText(_translate("Dialog", "Отмена"))
