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
        Dialog.resize(469, 311)
        font = QtGui.QFont()
        font.setPointSize(13)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.owner_edit = QtWidgets.QLineEdit(self.groupBox)
        self.owner_edit.setObjectName("owner_edit")
        self.gridLayout.addWidget(self.owner_edit, 3, 1, 1, 1)
        self.serial_number_edit = QtWidgets.QLineEdit(self.groupBox)
        self.serial_number_edit.setObjectName("serial_number_edit")
        self.gridLayout.addWidget(self.serial_number_edit, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 1, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)
        self.temperature_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.temperature_edit.setObjectName("temperature_edit")
        self.gridLayout_2.addWidget(self.temperature_edit, 1, 0, 1, 1)
        self.wet_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.wet_edit.setObjectName("wet_edit")
        self.gridLayout_2.addWidget(self.wet_edit, 1, 1, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 0, 0, 1, 1)
        self.pressure_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.pressure_edit.setObjectName("pressure_edit")
        self.gridLayout_2.addWidget(self.pressure_edit, 3, 0, 1, 1)
        self.warming_up_time_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.warming_up_time_edit.setObjectName("warming_up_time_edit")
        self.gridLayout_2.addWidget(self.warming_up_time_edit, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
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
        self.groupBox.setTitle(_translate("Dialog", "Общая информация"))
        self.label_3.setText(_translate("Dialog", "Заводской номер"))
        self.label_2.setText(_translate("Dialog", "Организация-владелец"))
        self.groupBox_2.setTitle(_translate("Dialog", "Условия поверки"))
        self.label_9.setText(_translate("Dialog", "Влажность, %"))
        self.label_12.setText(_translate("Dialog", "Давление, кПа"))
        self.label_11.setText(_translate("Dialog", "Прогрев прибора, мин"))
        self.label_10.setText(_translate("Dialog", "Температура, °С"))
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.reject_button.setText(_translate("Dialog", "Отмена"))