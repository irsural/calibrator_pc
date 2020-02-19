# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/template_list_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(601, 382)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.choose_templates_widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_templates_widget.sizePolicy().hasHeightForWidth())
        self.choose_templates_widget.setSizePolicy(sizePolicy)
        self.choose_templates_widget.setMaximumSize(QtCore.QSize(150, 16777215))
        self.choose_templates_widget.setObjectName("choose_templates_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.choose_templates_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.filter_edit = QtWidgets.QLineEdit(self.choose_templates_widget)
        self.filter_edit.setObjectName("filter_edit")
        self.horizontalLayout_3.addWidget(self.filter_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.templates_list = QtWidgets.QListWidget(self.choose_templates_widget)
        self.templates_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.templates_list.setObjectName("templates_list")
        self.verticalLayout_2.addWidget(self.templates_list)
        self.choose_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.choose_template_button.setObjectName("choose_template_button")
        self.verticalLayout_2.addWidget(self.choose_template_button)
        self.horizontalLayout.addWidget(self.choose_templates_widget)
        self.template_params_widget = QtWidgets.QFrame(Dialog)
        self.template_params_widget.setFrameShape(QtWidgets.QFrame.Panel)
        self.template_params_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.template_params_widget.setObjectName("template_params_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.template_params_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.template_params_widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.info_layout = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_layout.sizePolicy().hasHeightForWidth())
        self.info_layout.setSizePolicy(sizePolicy)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.info_layout)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.info_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 9, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 2)
        self.template_name_edit = QtWidgets.QLineEdit(self.frame)
        self.template_name_edit.setObjectName("template_name_edit")
        self.gridLayout.addWidget(self.template_name_edit, 2, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 14, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 12, 0, 1, 2)
        self.device_name_edit = QtWidgets.QLineEdit(self.frame)
        self.device_name_edit.setObjectName("device_name_edit")
        self.gridLayout.addWidget(self.device_name_edit, 8, 0, 1, 2)
        self.device_creator_edit = QtWidgets.QLineEdit(self.frame)
        self.device_creator_edit.setObjectName("device_creator_edit")
        self.gridLayout.addWidget(self.device_creator_edit, 11, 0, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 3, 0, 1, 2)
        self.organisation_edit = QtWidgets.QLineEdit(self.frame)
        self.organisation_edit.setText("")
        self.organisation_edit.setReadOnly(False)
        self.organisation_edit.setObjectName("organisation_edit")
        self.gridLayout.addWidget(self.organisation_edit, 4, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 2)
        self.device_system_combobox = QtWidgets.QComboBox(self.frame)
        self.device_system_combobox.setObjectName("device_system_combobox")
        self.device_system_combobox.addItem("")
        self.device_system_combobox.addItem("")
        self.device_system_combobox.addItem("")
        self.gridLayout.addWidget(self.device_system_combobox, 13, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 14, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 10, 0, 1, 2)
        self.class_spinbox = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.class_spinbox.sizePolicy().hasHeightForWidth())
        self.class_spinbox.setSizePolicy(sizePolicy)
        self.class_spinbox.setDecimals(4)
        self.class_spinbox.setMinimum(0.001)
        self.class_spinbox.setMaximum(10.0)
        self.class_spinbox.setSingleStep(0.05)
        self.class_spinbox.setProperty("value", 1.5)
        self.class_spinbox.setObjectName("class_spinbox")
        self.gridLayout.addWidget(self.class_spinbox, 15, 1, 1, 1)
        self.signal_type_combobox = QtWidgets.QComboBox(self.frame)
        self.signal_type_combobox.setObjectName("signal_type_combobox")
        self.signal_type_combobox.addItem("")
        self.signal_type_combobox.addItem("")
        self.signal_type_combobox.addItem("")
        self.signal_type_combobox.addItem("")
        self.gridLayout.addWidget(self.signal_type_combobox, 15, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 2)
        self.etalon_device_edit = QtWidgets.QLineEdit(self.frame)
        self.etalon_device_edit.setReadOnly(False)
        self.etalon_device_edit.setObjectName("etalon_device_edit")
        self.gridLayout.addWidget(self.etalon_device_edit, 6, 0, 1, 2)
        self.verticalLayout.addWidget(self.frame)
        self.verticalWidget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.points_table = QtWidgets.QTableWidget(self.verticalWidget)
        self.points_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.points_table.setObjectName("points_table")
        self.points_table.setColumnCount(2)
        self.points_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.points_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.points_table.setHorizontalHeaderItem(1, item)
        self.gridLayout_3.addWidget(self.points_table, 1, 0, 1, 3)
        self.cancel_edit_template_button = QtWidgets.QPushButton(self.verticalWidget)
        self.cancel_edit_template_button.setObjectName("cancel_edit_template_button")
        self.gridLayout_3.addWidget(self.cancel_edit_template_button, 2, 2, 1, 1)
        self.save_template_button = QtWidgets.QPushButton(self.verticalWidget)
        self.save_template_button.setObjectName("save_template_button")
        self.gridLayout_3.addWidget(self.save_template_button, 2, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_point_button = QtWidgets.QPushButton(self.verticalWidget)
        self.add_point_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.add_point_button.setFont(font)
        self.add_point_button.setObjectName("add_point_button")
        self.horizontalLayout_2.addWidget(self.add_point_button)
        self.remove_point_button = QtWidgets.QPushButton(self.verticalWidget)
        self.remove_point_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.remove_point_button.setFont(font)
        self.remove_point_button.setObjectName("remove_point_button")
        self.horizontalLayout_2.addWidget(self.remove_point_button)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.template_params_widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.filter_edit, self.templates_list)
        Dialog.setTabOrder(self.templates_list, self.template_name_edit)
        Dialog.setTabOrder(self.template_name_edit, self.organisation_edit)
        Dialog.setTabOrder(self.organisation_edit, self.etalon_device_edit)
        Dialog.setTabOrder(self.etalon_device_edit, self.device_name_edit)
        Dialog.setTabOrder(self.device_name_edit, self.device_creator_edit)
        Dialog.setTabOrder(self.device_creator_edit, self.device_system_combobox)
        Dialog.setTabOrder(self.device_system_combobox, self.signal_type_combobox)
        Dialog.setTabOrder(self.signal_type_combobox, self.class_spinbox)
        Dialog.setTabOrder(self.class_spinbox, self.add_point_button)
        Dialog.setTabOrder(self.add_point_button, self.remove_point_button)
        Dialog.setTabOrder(self.remove_point_button, self.points_table)
        Dialog.setTabOrder(self.points_table, self.choose_template_button)
        Dialog.setTabOrder(self.choose_template_button, self.save_template_button)
        Dialog.setTabOrder(self.save_template_button, self.cancel_edit_template_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Выбор шаблона"))
        self.filter_edit.setPlaceholderText(_translate("Dialog", "Поиск..."))
        self.templates_list.setSortingEnabled(False)
        self.choose_template_button.setText(_translate("Dialog", "Выбрать"))
        self.label_7.setText(_translate("Dialog", "Средство поверки"))
        self.label.setText(_translate("Dialog", "Класс"))
        self.label_2.setText(_translate("Dialog", "Система прибора"))
        self.label_13.setText(_translate("Dialog", "Организация-поверитель"))
        self.label_4.setText(_translate("Dialog", "Наименование прибора"))
        self.device_system_combobox.setItemText(0, _translate("Dialog", "Магнитоэлектрическая"))
        self.device_system_combobox.setItemText(1, _translate("Dialog", "Электродинамическая"))
        self.device_system_combobox.setItemText(2, _translate("Dialog", "Электромагнитная"))
        self.label_8.setText(_translate("Dialog", "Род тока"))
        self.label_5.setText(_translate("Dialog", "Изготовитель прибора"))
        self.signal_type_combobox.setItemText(0, _translate("Dialog", "I~"))
        self.signal_type_combobox.setItemText(1, _translate("Dialog", "U~"))
        self.signal_type_combobox.setItemText(2, _translate("Dialog", "I="))
        self.signal_type_combobox.setItemText(3, _translate("Dialog", "U="))
        self.label_6.setText(_translate("Dialog", "Название шаблона"))
        self.etalon_device_edit.setText(_translate("Dialog", "Калибратор N4-25"))
        item = self.points_table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Амплитуда"))
        item = self.points_table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Частота, Гц"))
        self.cancel_edit_template_button.setText(_translate("Dialog", "Отмена"))
        self.save_template_button.setText(_translate("Dialog", "Сохранить"))
        self.add_point_button.setText(_translate("Dialog", "+"))
        self.remove_point_button.setText(_translate("Dialog", "-"))
        self.label_3.setText(_translate("Dialog", "Точки поверки"))
