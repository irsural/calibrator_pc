# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/on_run_edit_template_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 436)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.temperature_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temperature_edit.sizePolicy().hasHeightForWidth())
        self.temperature_edit.setSizePolicy(sizePolicy)
        self.temperature_edit.setObjectName("temperature_edit")
        self.gridLayout.addWidget(self.temperature_edit, 7, 0, 1, 1)
        self.creator_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creator_edit.sizePolicy().hasHeightForWidth())
        self.creator_edit.setSizePolicy(sizePolicy)
        self.creator_edit.setObjectName("creator_edit")
        self.gridLayout.addWidget(self.creator_edit, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.owner_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.owner_edit.sizePolicy().hasHeightForWidth())
        self.owner_edit.setSizePolicy(sizePolicy)
        self.owner_edit.setObjectName("owner_edit")
        self.gridLayout.addWidget(self.owner_edit, 5, 1, 1, 1)
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
        self.gridLayout.addWidget(self.system_combobox, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 2, 1, 1)
        self.warming_up_time_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warming_up_time_edit.sizePolicy().hasHeightForWidth())
        self.warming_up_time_edit.setSizePolicy(sizePolicy)
        self.warming_up_time_edit.setObjectName("warming_up_time_edit")
        self.gridLayout.addWidget(self.warming_up_time_edit, 5, 2, 1, 1)
        self.organisation_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.organisation_edit.sizePolicy().hasHeightForWidth())
        self.organisation_edit.setSizePolicy(sizePolicy)
        self.organisation_edit.setText("")
        self.organisation_edit.setReadOnly(False)
        self.organisation_edit.setObjectName("organisation_edit")
        self.gridLayout.addWidget(self.organisation_edit, 5, 0, 1, 1)
        self.name_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy)
        self.name_edit.setObjectName("name_edit")
        self.gridLayout.addWidget(self.name_edit, 3, 0, 1, 1)
        self.pressure_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pressure_edit.sizePolicy().hasHeightForWidth())
        self.pressure_edit.setSizePolicy(sizePolicy)
        self.pressure_edit.setObjectName("pressure_edit")
        self.gridLayout.addWidget(self.pressure_edit, 7, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 4, 0, 1, 1)
        self.serial_number_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_edit.sizePolicy().hasHeightForWidth())
        self.serial_number_edit.setSizePolicy(sizePolicy)
        self.serial_number_edit.setObjectName("serial_number_edit")
        self.gridLayout.addWidget(self.serial_number_edit, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.user_name_edit = QtWidgets.QLineEdit(self.groupBox)
        self.user_name_edit.setObjectName("user_name_edit")
        self.gridLayout.addWidget(self.user_name_edit, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 6, 2, 1, 1)
        self.date_edit = QtWidgets.QDateTimeEdit(self.groupBox)
        self.date_edit.setObjectName("date_edit")
        self.gridLayout.addWidget(self.date_edit, 1, 2, 1, 1)
        self.wet_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wet_edit.sizePolicy().hasHeightForWidth())
        self.wet_edit.setSizePolicy(sizePolicy)
        self.wet_edit.setObjectName("wet_edit")
        self.gridLayout.addWidget(self.wet_edit, 7, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 6, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 9, 0, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.marks_table = QtWidgets.QTableWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.marks_table.sizePolicy().hasHeightForWidth())
        self.marks_table.setSizePolicy(sizePolicy)
        self.marks_table.setObjectName("marks_table")
        self.marks_table.setColumnCount(3)
        self.marks_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.marks_table)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.add_mark_button = QtWidgets.QPushButton(self.widget_2)
        self.add_mark_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.add_mark_button.setFont(font)
        self.add_mark_button.setObjectName("add_mark_button")
        self.verticalLayout_3.addWidget(self.add_mark_button)
        self.remove_mark_button = QtWidgets.QPushButton(self.widget_2)
        self.remove_mark_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.remove_mark_button.setFont(font)
        self.remove_mark_button.setObjectName("remove_mark_button")
        self.verticalLayout_3.addWidget(self.remove_mark_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
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
        Dialog.setWindowTitle(_translate("Dialog", "Редактирование шаблона во время поверки"))
        self.label.setText(_translate("Dialog", "Поверитель"))
        self.system_combobox.setItemText(0, _translate("Dialog", "Магнитоэлектрическая"))
        self.system_combobox.setItemText(1, _translate("Dialog", "Электродинамическая"))
        self.system_combobox.setItemText(2, _translate("Dialog", "Электромагнитная"))
        self.label_3.setText(_translate("Dialog", "Организация-владелец"))
        self.label_4.setText(_translate("Dialog", "Наименование"))
        self.label_7.setText(_translate("Dialog", "Заводской номер"))
        self.label_11.setText(_translate("Dialog", "Прогрев прибора, мин"))
        self.label_13.setText(_translate("Dialog", "Организация-поверитель"))
        self.label_10.setText(_translate("Dialog", "Температура, °С"))
        self.label_2.setText(_translate("Dialog", "Система"))
        self.label_6.setText(_translate("Dialog", "Дата поверки"))
        self.label_12.setText(_translate("Dialog", "Давление, кПа"))
        self.date_edit.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy"))
        self.label_5.setText(_translate("Dialog", "Изготовитель"))
        self.label_9.setText(_translate("Dialog", "Влажность, %"))
        item = self.marks_table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Описание"))
        item = self.marks_table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Метка"))
        item = self.marks_table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Значение"))
        self.add_mark_button.setText(_translate("Dialog", "+"))
        self.remove_mark_button.setText(_translate("Dialog", "-"))
        self.accept_button.setText(_translate("Dialog", "Сохранить"))
        self.reject_button.setText(_translate("Dialog", "Отмена"))
