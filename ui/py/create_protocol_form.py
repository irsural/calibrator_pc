# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_protocol_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_create_protocol_dialog(object):
    def setupUi(self, create_protocol_dialog):
        create_protocol_dialog.setObjectName("create_protocol_dialog")
        create_protocol_dialog.resize(1052, 595)
        font = QtGui.QFont()
        font.setPointSize(10)
        create_protocol_dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(create_protocol_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_12 = QtWidgets.QLabel(create_protocol_dialog)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)
        self.template_protocol_edit = QtWidgets.QLineEdit(create_protocol_dialog)
        self.template_protocol_edit.setObjectName("template_protocol_edit")
        self.gridLayout_3.addWidget(self.template_protocol_edit, 0, 1, 1, 1)
        self.save_folder_edit = QtWidgets.QLineEdit(create_protocol_dialog)
        self.save_folder_edit.setObjectName("save_folder_edit")
        self.gridLayout_3.addWidget(self.save_folder_edit, 1, 1, 1, 1)
        self.choose_protocol_template_button = QtWidgets.QToolButton(create_protocol_dialog)
        self.choose_protocol_template_button.setObjectName("choose_protocol_template_button")
        self.gridLayout_3.addWidget(self.choose_protocol_template_button, 0, 2, 1, 1)
        self.choose_save_folder_button = QtWidgets.QToolButton(create_protocol_dialog)
        self.choose_save_folder_button.setObjectName("choose_save_folder_button")
        self.gridLayout_3.addWidget(self.choose_save_folder_button, 1, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(create_protocol_dialog)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.splitter = QtWidgets.QSplitter(create_protocol_dialog)
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
        self.serial_number_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_label.sizePolicy().hasHeightForWidth())
        self.serial_number_label.setSizePolicy(sizePolicy)
        self.serial_number_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.serial_number_label.setObjectName("serial_number_label")
        self.gridLayout.addWidget(self.serial_number_label, 2, 1, 1, 1)
        self.serial_number_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_number_edit.sizePolicy().hasHeightForWidth())
        self.serial_number_edit.setSizePolicy(sizePolicy)
        self.serial_number_edit.setObjectName("serial_number_edit")
        self.gridLayout.addWidget(self.serial_number_edit, 3, 1, 1, 1)
        self.date_edit = QtWidgets.QDateTimeEdit(self.groupBox)
        self.date_edit.setObjectName("date_edit")
        self.gridLayout.addWidget(self.date_edit, 7, 0, 1, 1)
        self.date_label = QtWidgets.QLabel(self.groupBox)
        self.date_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.date_label.setObjectName("date_label")
        self.gridLayout.addWidget(self.date_label, 6, 0, 1, 1)
        self.system_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.system_label.sizePolicy().hasHeightForWidth())
        self.system_label.setSizePolicy(sizePolicy)
        self.system_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.system_label.setObjectName("system_label")
        self.gridLayout.addWidget(self.system_label, 0, 2, 1, 1)
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
        self.owner_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.owner_label.sizePolicy().hasHeightForWidth())
        self.owner_label.setSizePolicy(sizePolicy)
        self.owner_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.owner_label.setObjectName("owner_label")
        self.gridLayout.addWidget(self.owner_label, 2, 2, 1, 1)
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
        self.user_label = QtWidgets.QLabel(self.groupBox)
        self.user_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.user_label.setObjectName("user_label")
        self.gridLayout.addWidget(self.user_label, 2, 0, 1, 1)
        self.name_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        self.name_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.device_name_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_name_edit.sizePolicy().hasHeightForWidth())
        self.device_name_edit.setSizePolicy(sizePolicy)
        self.device_name_edit.setObjectName("device_name_edit")
        self.gridLayout.addWidget(self.device_name_edit, 1, 0, 1, 1)
        self.device_creator_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_creator_label.sizePolicy().hasHeightForWidth())
        self.device_creator_label.setSizePolicy(sizePolicy)
        self.device_creator_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.device_creator_label.setObjectName("device_creator_label")
        self.gridLayout.addWidget(self.device_creator_label, 0, 1, 1, 1)
        self.device_creator_edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_creator_edit.sizePolicy().hasHeightForWidth())
        self.device_creator_edit.setSizePolicy(sizePolicy)
        self.device_creator_edit.setObjectName("device_creator_edit")
        self.gridLayout.addWidget(self.device_creator_edit, 1, 1, 1, 1)
        self.comment_edit = QtWidgets.QLineEdit(self.groupBox)
        self.comment_edit.setObjectName("comment_edit")
        self.gridLayout.addWidget(self.comment_edit, 7, 1, 1, 2)
        self.comment_label = QtWidgets.QLabel(self.groupBox)
        self.comment_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.comment_label.setObjectName("comment_label")
        self.gridLayout.addWidget(self.comment_label, 6, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.splitter)
        self.marks_and_points_tabwidget = QtWidgets.QTabWidget(create_protocol_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.marks_and_points_tabwidget.sizePolicy().hasHeightForWidth())
        self.marks_and_points_tabwidget.setSizePolicy(sizePolicy)
        self.marks_and_points_tabwidget.setObjectName("marks_and_points_tabwidget")
        self.marks_widget_tab = QtWidgets.QWidget()
        self.marks_widget_tab.setObjectName("marks_widget_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.marks_widget_tab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.marks_widget_layout = QtWidgets.QVBoxLayout()
        self.marks_widget_layout.setObjectName("marks_widget_layout")
        self.gridLayout_4.addLayout(self.marks_widget_layout, 0, 0, 1, 1)
        self.marks_and_points_tabwidget.addTab(self.marks_widget_tab, "")
        self.points_tab = QtWidgets.QWidget()
        self.points_tab.setObjectName("points_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.points_tab)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.points_table = QtWidgets.QTableView(self.points_tab)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.points_table.setFont(font)
        self.points_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.points_table.setStyleSheet("selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(170, 170, 255);")
        self.points_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.points_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.points_table.setObjectName("points_table")
        self.gridLayout_5.addWidget(self.points_table, 1, 0, 1, 1)
        self.cases_bar_layout = QtWidgets.QVBoxLayout()
        self.cases_bar_layout.setObjectName("cases_bar_layout")
        self.gridLayout_5.addLayout(self.cases_bar_layout, 0, 0, 1, 1)
        self.marks_and_points_tabwidget.addTab(self.points_tab, "")
        self.verticalLayout.addWidget(self.marks_and_points_tabwidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.default_button = QtWidgets.QPushButton(create_protocol_dialog)
        self.default_button.setEnabled(False)
        self.default_button.setDefault(True)
        self.default_button.setObjectName("default_button")
        self.horizontalLayout_2.addWidget(self.default_button)
        self.to_excel_button = QtWidgets.QPushButton(create_protocol_dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/excel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.to_excel_button.setIcon(icon)
        self.to_excel_button.setIconSize(QtCore.QSize(20, 20))
        self.to_excel_button.setObjectName("to_excel_button")
        self.horizontalLayout_2.addWidget(self.to_excel_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.accept_button = QtWidgets.QPushButton(create_protocol_dialog)
        self.accept_button.setAutoDefault(False)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_2.addWidget(self.accept_button)
        self.reject_button = QtWidgets.QPushButton(create_protocol_dialog)
        self.reject_button.setAutoDefault(False)
        self.reject_button.setObjectName("reject_button")
        self.horizontalLayout_2.addWidget(self.reject_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(create_protocol_dialog)
        self.marks_and_points_tabwidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(create_protocol_dialog)
        create_protocol_dialog.setTabOrder(self.template_protocol_edit, self.choose_protocol_template_button)
        create_protocol_dialog.setTabOrder(self.choose_protocol_template_button, self.save_folder_edit)
        create_protocol_dialog.setTabOrder(self.save_folder_edit, self.choose_save_folder_button)
        create_protocol_dialog.setTabOrder(self.choose_save_folder_button, self.device_name_edit)
        create_protocol_dialog.setTabOrder(self.device_name_edit, self.device_creator_edit)
        create_protocol_dialog.setTabOrder(self.device_creator_edit, self.system_combobox)
        create_protocol_dialog.setTabOrder(self.system_combobox, self.user_name_edit)
        create_protocol_dialog.setTabOrder(self.user_name_edit, self.serial_number_edit)
        create_protocol_dialog.setTabOrder(self.serial_number_edit, self.owner_edit)
        create_protocol_dialog.setTabOrder(self.owner_edit, self.date_edit)
        create_protocol_dialog.setTabOrder(self.date_edit, self.comment_edit)
        create_protocol_dialog.setTabOrder(self.comment_edit, self.marks_and_points_tabwidget)
        create_protocol_dialog.setTabOrder(self.marks_and_points_tabwidget, self.points_table)
        create_protocol_dialog.setTabOrder(self.points_table, self.accept_button)
        create_protocol_dialog.setTabOrder(self.accept_button, self.reject_button)
        create_protocol_dialog.setTabOrder(self.reject_button, self.default_button)

    def retranslateUi(self, create_protocol_dialog):
        _translate = QtCore.QCoreApplication.translate
        create_protocol_dialog.setWindowTitle(_translate("create_protocol_dialog", "Создание протокола поверки"))
        self.label_12.setText(_translate("create_protocol_dialog", "Шаблон протокола"))
        self.choose_protocol_template_button.setText(_translate("create_protocol_dialog", "..."))
        self.choose_save_folder_button.setText(_translate("create_protocol_dialog", "..."))
        self.label_14.setText(_translate("create_protocol_dialog", "Каталог сохранения"))
        self.serial_number_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Заводской номер (<span style=\" color:#ff557f;\">%serial__</span>)</p></body></html>"))
        self.date_edit.setDisplayFormat(_translate("create_protocol_dialog", "dd.MM.yyyy"))
        self.date_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Дата поверки (<span style=\" color:#ff557f;\">%date__</span>)</p></body></html>"))
        self.system_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Система (<span style=\" color:#ff557f;\">%system__</span>)</p></body></html>"))
        self.system_combobox.setItemText(0, _translate("create_protocol_dialog", "Магнитоэлектрическая"))
        self.system_combobox.setItemText(1, _translate("create_protocol_dialog", "Электродинамическая"))
        self.system_combobox.setItemText(2, _translate("create_protocol_dialog", "Электромагнитная"))
        self.owner_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Орг.-владелец (<span style=\" color:#ff557f;\">%owner__</span>)</p></body></html>"))
        self.user_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Поверитель (<span style=\" color:#ff557f;\">%user__</span>)</p></body></html>"))
        self.name_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Наименование (<span style=\" color:#ff557f;\">%name__</span>)</p></body></html>"))
        self.device_creator_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Изготовитель (<span style=\" color:#ff557f;\">%creator__</span>)</p></body></html>"))
        self.comment_label.setText(_translate("create_protocol_dialog", "<html><head/><body><p>Комментарий (<span style=\" color:#ff557f;\">%comment__</span>)</p></body></html>"))
        self.marks_and_points_tabwidget.setTabText(self.marks_and_points_tabwidget.indexOf(self.marks_widget_tab), _translate("create_protocol_dialog", "Дополнительные параметры"))
        self.marks_and_points_tabwidget.setTabText(self.marks_and_points_tabwidget.indexOf(self.points_tab), _translate("create_protocol_dialog", "Результаты измерения"))
        self.default_button.setText(_translate("create_protocol_dialog", "default"))
        self.to_excel_button.setText(_translate("create_protocol_dialog", "Скопировать в формате Excel"))
        self.accept_button.setText(_translate("create_protocol_dialog", "Сохранить и создать отчет"))
        self.reject_button.setText(_translate("create_protocol_dialog", "Отмена"))
import icons
