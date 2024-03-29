# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_list_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_templates_list_dialog(object):
    def setupUi(self, templates_list_dialog):
        templates_list_dialog.setObjectName("templates_list_dialog")
        templates_list_dialog.resize(627, 420)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(templates_list_dialog.sizePolicy().hasHeightForWidth())
        templates_list_dialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        templates_list_dialog.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(templates_list_dialog)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.choose_templates_widget = QtWidgets.QWidget(templates_list_dialog)
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.duplicate_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.duplicate_template_button.setMinimumSize(QtCore.QSize(34, 0))
        self.duplicate_template_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/duplicate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.duplicate_template_button.setIcon(icon)
        self.duplicate_template_button.setObjectName("duplicate_template_button")
        self.horizontalLayout_4.addWidget(self.duplicate_template_button)
        self.edit_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.edit_template_button.setMinimumSize(QtCore.QSize(34, 0))
        self.edit_template_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_template_button.setIcon(icon1)
        self.edit_template_button.setObjectName("edit_template_button")
        self.horizontalLayout_4.addWidget(self.edit_template_button)
        self.add_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.add_template_button.setMinimumSize(QtCore.QSize(34, 0))
        self.add_template_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_template_button.setIcon(icon2)
        self.add_template_button.setObjectName("add_template_button")
        self.horizontalLayout_4.addWidget(self.add_template_button)
        self.delete_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.delete_template_button.setMinimumSize(QtCore.QSize(34, 0))
        self.delete_template_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/minus2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_template_button.setIcon(icon3)
        self.delete_template_button.setObjectName("delete_template_button")
        self.horizontalLayout_4.addWidget(self.delete_template_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.templates_list = QtWidgets.QListWidget(self.choose_templates_widget)
        self.templates_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.templates_list.setStyleSheet("selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(170, 170, 255);")
        self.templates_list.setObjectName("templates_list")
        self.verticalLayout_2.addWidget(self.templates_list)
        self.choose_template_button = QtWidgets.QPushButton(self.choose_templates_widget)
        self.choose_template_button.setObjectName("choose_template_button")
        self.verticalLayout_2.addWidget(self.choose_template_button)
        self.horizontalLayout.addWidget(self.choose_templates_widget)
        self.template_params_widget = QtWidgets.QFrame(templates_list_dialog)
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
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_layout.sizePolicy().hasHeightForWidth())
        self.info_layout.setSizePolicy(sizePolicy)
        self.info_layout.setObjectName("info_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.info_layout)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.info_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 9, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.device_system_combobox = QtWidgets.QComboBox(self.frame)
        self.device_system_combobox.setObjectName("device_system_combobox")
        self.device_system_combobox.addItem("")
        self.device_system_combobox.addItem("")
        self.device_system_combobox.addItem("")
        self.gridLayout.addWidget(self.device_system_combobox, 9, 0, 1, 2)
        self.device_name_edit = QtWidgets.QLineEdit(self.frame)
        self.device_name_edit.setObjectName("device_name_edit")
        self.gridLayout.addWidget(self.device_name_edit, 4, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 2)
        self.template_name_edit = QtWidgets.QLineEdit(self.frame)
        self.template_name_edit.setObjectName("template_name_edit")
        self.gridLayout.addWidget(self.template_name_edit, 2, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 2)
        self.device_creator_edit = QtWidgets.QLineEdit(self.frame)
        self.device_creator_edit.setObjectName("device_creator_edit")
        self.gridLayout.addWidget(self.device_creator_edit, 7, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 2)
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
        self.cancel_edit_template_button = QtWidgets.QPushButton(self.verticalWidget)
        self.cancel_edit_template_button.setAutoDefault(False)
        self.cancel_edit_template_button.setObjectName("cancel_edit_template_button")
        self.gridLayout_3.addWidget(self.cancel_edit_template_button, 2, 2, 1, 1)
        self.save_template_button = QtWidgets.QPushButton(self.verticalWidget)
        self.save_template_button.setAutoDefault(False)
        self.save_template_button.setObjectName("save_template_button")
        self.gridLayout_3.addWidget(self.save_template_button, 2, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scales_layout = QtWidgets.QVBoxLayout()
        self.scales_layout.setContentsMargins(0, 0, 0, 0)
        self.scales_layout.setObjectName("scales_layout")
        self.gridLayout_4.addLayout(self.scales_layout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.widget, 1, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.verticalWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 3)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.template_params_widget)

        self.retranslateUi(templates_list_dialog)
        QtCore.QMetaObject.connectSlotsByName(templates_list_dialog)
        templates_list_dialog.setTabOrder(self.filter_edit, self.duplicate_template_button)
        templates_list_dialog.setTabOrder(self.duplicate_template_button, self.edit_template_button)
        templates_list_dialog.setTabOrder(self.edit_template_button, self.add_template_button)
        templates_list_dialog.setTabOrder(self.add_template_button, self.delete_template_button)
        templates_list_dialog.setTabOrder(self.delete_template_button, self.templates_list)
        templates_list_dialog.setTabOrder(self.templates_list, self.choose_template_button)
        templates_list_dialog.setTabOrder(self.choose_template_button, self.template_name_edit)
        templates_list_dialog.setTabOrder(self.template_name_edit, self.device_name_edit)
        templates_list_dialog.setTabOrder(self.device_name_edit, self.device_creator_edit)
        templates_list_dialog.setTabOrder(self.device_creator_edit, self.device_system_combobox)
        templates_list_dialog.setTabOrder(self.device_system_combobox, self.save_template_button)
        templates_list_dialog.setTabOrder(self.save_template_button, self.cancel_edit_template_button)

    def retranslateUi(self, templates_list_dialog):
        _translate = QtCore.QCoreApplication.translate
        templates_list_dialog.setWindowTitle(_translate("templates_list_dialog", "Выбор шаблона"))
        self.filter_edit.setPlaceholderText(_translate("templates_list_dialog", "Поиск..."))
        self.templates_list.setSortingEnabled(False)
        self.choose_template_button.setText(_translate("templates_list_dialog", "Выбрать"))
        self.device_system_combobox.setItemText(0, _translate("templates_list_dialog", "Магнитоэлектрическая"))
        self.device_system_combobox.setItemText(1, _translate("templates_list_dialog", "Электродинамическая"))
        self.device_system_combobox.setItemText(2, _translate("templates_list_dialog", "Электромагнитная"))
        self.label_4.setText(_translate("templates_list_dialog", "Наименование прибора"))
        self.label_6.setText(_translate("templates_list_dialog", "Название шаблона"))
        self.label_5.setText(_translate("templates_list_dialog", "Изготовитель прибора"))
        self.label_2.setText(_translate("templates_list_dialog", "Система прибора"))
        self.cancel_edit_template_button.setText(_translate("templates_list_dialog", "Отмена"))
        self.save_template_button.setText(_translate("templates_list_dialog", "Сохранить"))
        self.label_3.setText(_translate("templates_list_dialog", "Шкалы прибора"))
import icons
