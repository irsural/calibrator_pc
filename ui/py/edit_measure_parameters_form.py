# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/edit_measure_parameters_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(503, 431)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.device_creator_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_creator_edit.sizePolicy().hasHeightForWidth())
        self.device_creator_edit.setSizePolicy(sizePolicy)
        self.device_creator_edit.setObjectName("device_creator_edit")
        self.gridLayout.addWidget(self.device_creator_edit, 1, 1, 1, 1)
        self.system_combobox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.system_combobox.sizePolicy().hasHeightForWidth())
        self.system_combobox.setSizePolicy(sizePolicy)
        self.system_combobox.setObjectName("system_combobox")
        self.system_combobox.addItem("")
        self.system_combobox.addItem("")
        self.system_combobox.addItem("")
        self.gridLayout.addWidget(self.system_combobox, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.device_name_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_name_edit.sizePolicy().hasHeightForWidth())
        self.device_name_edit.setSizePolicy(sizePolicy)
        self.device_name_edit.setObjectName("device_name_edit")
        self.gridLayout.addWidget(self.device_name_edit, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.owner_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.owner_edit.sizePolicy().hasHeightForWidth())
        self.owner_edit.setSizePolicy(sizePolicy)
        self.owner_edit.setObjectName("owner_edit")
        self.gridLayout.addWidget(self.owner_edit, 3, 2, 1, 1)
        self.user_name_edit = QtWidgets.QLineEdit(self.groupBox)
        self.user_name_edit.setObjectName("user_name_edit")
        self.gridLayout.addWidget(self.user_name_edit, 3, 0, 1, 1)
        self.date_edit = QtWidgets.QDateTimeEdit(self.groupBox)
        self.date_edit.setObjectName("date_edit")
        self.gridLayout.addWidget(self.date_edit, 5, 0, 1, 1)
        self.serial_number_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_edit.sizePolicy().hasHeightForWidth())
        self.serial_number_edit.setSizePolicy(sizePolicy)
        self.serial_number_edit.setObjectName("serial_number_edit")
        self.gridLayout.addWidget(self.serial_number_edit, 3, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 2)
        self.comment_edit = QtWidgets.QLineEdit(self.groupBox)
        self.comment_edit.setObjectName("comment_edit")
        self.gridLayout.addWidget(self.comment_edit, 5, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.marks_widget_layout = QtWidgets.QVBoxLayout()
        self.marks_widget_layout.setObjectName("marks_widget_layout")
        self.horizontalLayout.addLayout(self.marks_widget_layout)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.default_button = QtWidgets.QPushButton(Dialog)
        self.default_button.setEnabled(False)
        self.default_button.setDefault(True)
        self.default_button.setObjectName("default_button")
        self.horizontalLayout_2.addWidget(self.default_button)
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
        Dialog.setTabOrder(self.accept_button, self.reject_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Редактирование параметров измерения"))
        self.label_5.setText(_translate("Dialog", "Изготовитель"))
        self.system_combobox.setItemText(0, _translate("Dialog", "Магнитоэлектрическая"))
        self.system_combobox.setItemText(1, _translate("Dialog", "Электродинамическая"))
        self.system_combobox.setItemText(2, _translate("Dialog", "Электромагнитная"))
        self.label_6.setText(_translate("Dialog", "Дата поверки"))
        self.label.setText(_translate("Dialog", "Поверитель"))
        self.label_7.setText(_translate("Dialog", "Заводской номер"))
        self.label_2.setText(_translate("Dialog", "Система"))
        self.label_3.setText(_translate("Dialog", "Организация-владелец"))
        self.label_4.setText(_translate("Dialog", "Наименование"))
        self.date_edit.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy"))
        self.label_8.setText(_translate("Dialog", "Комментарий"))
        self.default_button.setText(_translate("Dialog", "default"))
        self.accept_button.setText(_translate("Dialog", "Сохранить"))
        self.reject_button.setText(_translate("Dialog", "Отмена"))
