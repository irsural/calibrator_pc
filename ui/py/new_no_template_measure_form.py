# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/new_no_template_measure_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(299, 414)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.aci_radio = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.aci_radio.setFont(font)
        self.aci_radio.setChecked(True)
        self.aci_radio.setObjectName("aci_radio")
        self.signal_type_group = QtWidgets.QButtonGroup(Dialog)
        self.signal_type_group.setObjectName("signal_type_group")
        self.signal_type_group.addButton(self.aci_radio)
        self.horizontalLayout.addWidget(self.aci_radio)
        self.acv_radio = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.acv_radio.setFont(font)
        self.acv_radio.setObjectName("acv_radio")
        self.signal_type_group.addButton(self.acv_radio)
        self.horizontalLayout.addWidget(self.acv_radio)
        self.dci_radio = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dci_radio.setFont(font)
        self.dci_radio.setChecked(False)
        self.dci_radio.setObjectName("dci_radio")
        self.signal_type_group.addButton(self.dci_radio)
        self.horizontalLayout.addWidget(self.dci_radio)
        self.dcv_radio = QtWidgets.QRadioButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dcv_radio.setFont(font)
        self.dcv_radio.setChecked(False)
        self.dcv_radio.setObjectName("dcv_radio")
        self.signal_type_group.addButton(self.dcv_radio)
        self.horizontalLayout.addWidget(self.dcv_radio)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.line_2 = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.clb_list_combobox = QtWidgets.QComboBox(Dialog)
        self.clb_list_combobox.setMinimumSize(QtCore.QSize(127, 0))
        self.clb_list_combobox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clb_list_combobox.setFont(font)
        self.clb_list_combobox.setObjectName("clb_list_combobox")
        self.gridLayout.addWidget(self.clb_list_combobox, 1, 0, 1, 1)
        self.lower_bound_edit = QtWidgets.QLineEdit(Dialog)
        self.lower_bound_edit.setMinimumSize(QtCore.QSize(127, 0))
        self.lower_bound_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lower_bound_edit.setFont(font)
        self.lower_bound_edit.setObjectName("lower_bound_edit")
        self.gridLayout.addWidget(self.lower_bound_edit, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.upper_bound_edit = QtWidgets.QLineEdit(Dialog)
        self.upper_bound_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.upper_bound_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.upper_bound_edit.setFont(font)
        self.upper_bound_edit.setObjectName("upper_bound_edit")
        self.gridLayout.addWidget(self.upper_bound_edit, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 2, 1, 1)
        self.display_resolution_combobox = QtWidgets.QComboBox(Dialog)
        self.display_resolution_combobox.setMinimumSize(QtCore.QSize(0, 0))
        self.display_resolution_combobox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.display_resolution_combobox.setFont(font)
        self.display_resolution_combobox.setObjectName("display_resolution_combobox")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.display_resolution_combobox.addItem("")
        self.gridLayout.addWidget(self.display_resolution_combobox, 6, 0, 1, 1)
        self.accuracy_spinbox = QtWidgets.QSpinBox(Dialog)
        self.accuracy_spinbox.setMinimumSize(QtCore.QSize(0, 0))
        self.accuracy_spinbox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.accuracy_spinbox.setMinimum(1)
        self.accuracy_spinbox.setMaximum(50)
        self.accuracy_spinbox.setProperty("value", 10)
        self.accuracy_spinbox.setObjectName("accuracy_spinbox")
        self.gridLayout.addWidget(self.accuracy_spinbox, 6, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.auto_calc_points_checkbox = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auto_calc_points_checkbox.setFont(font)
        self.auto_calc_points_checkbox.setCheckable(True)
        self.auto_calc_points_checkbox.setChecked(False)
        self.auto_calc_points_checkbox.setObjectName("auto_calc_points_checkbox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.auto_calc_points_checkbox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frequency_edit = QtWidgets.QLineEdit(self.auto_calc_points_checkbox)
        self.frequency_edit.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frequency_edit.setFont(font)
        self.frequency_edit.setText("")
        self.frequency_edit.setReadOnly(True)
        self.frequency_edit.setClearButtonEnabled(False)
        self.frequency_edit.setObjectName("frequency_edit")
        self.horizontalLayout_2.addWidget(self.frequency_edit)
        self.edit_frequency_button = QtWidgets.QPushButton(self.auto_calc_points_checkbox)
        self.edit_frequency_button.setMinimumSize(QtCore.QSize(22, 24))
        self.edit_frequency_button.setMaximumSize(QtCore.QSize(22, 24))
        self.edit_frequency_button.setObjectName("edit_frequency_button")
        self.horizontalLayout_2.addWidget(self.edit_frequency_button)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.start_point_down_radio = QtWidgets.QRadioButton(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_point_down_radio.setFont(font)
        self.start_point_down_radio.setChecked(True)
        self.start_point_down_radio.setObjectName("start_point_down_radio")
        self.horizontalLayout_4.addWidget(self.start_point_down_radio)
        self.start_point_up_radio = QtWidgets.QRadioButton(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_point_up_radio.setFont(font)
        self.start_point_up_radio.setChecked(False)
        self.start_point_up_radio.setObjectName("start_point_up_radio")
        self.horizontalLayout_4.addWidget(self.start_point_up_radio)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 1, 1, 2)
        self.step_edit = QtWidgets.QLineEdit(self.auto_calc_points_checkbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_edit.sizePolicy().hasHeightForWidth())
        self.step_edit.setSizePolicy(sizePolicy)
        self.step_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.step_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step_edit.setFont(font)
        self.step_edit.setObjectName("step_edit")
        self.gridLayout_2.addWidget(self.step_edit, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.step_help_button = QtWidgets.QPushButton(self.auto_calc_points_checkbox)
        self.step_help_button.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step_help_button.setFont(font)
        self.step_help_button.setDefault(False)
        self.step_help_button.setObjectName("step_help_button")
        self.gridLayout_2.addWidget(self.step_help_button, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.auto_calc_points_checkbox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.accept_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accept_button.setFont(font)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_3.addWidget(self.accept_button)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_3.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.display_resolution_combobox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Измерение без шаблона"))
        self.label.setText(_translate("Dialog", "Режим"))
        self.aci_radio.setText(_translate("Dialog", "I~"))
        self.acv_radio.setText(_translate("Dialog", "U~"))
        self.dci_radio.setText(_translate("Dialog", "I="))
        self.dcv_radio.setText(_translate("Dialog", "U="))
        self.label_2.setText(_translate("Dialog", "Параметры поверки"))
        self.label_5.setText(_translate("Dialog", "Верхняя точка"))
        self.lower_bound_edit.setText(_translate("Dialog", "0"))
        self.label_3.setText(_translate("Dialog", "Нижняя точка"))
        self.label_8.setText(_translate("Dialog", "Калибратор"))
        self.upper_bound_edit.setText(_translate("Dialog", "1"))
        self.label_4.setText(_translate("Dialog", "Разрешение дисплея"))
        self.label_7.setText(_translate("Dialog", "Точность подхода, %"))
        self.display_resolution_combobox.setCurrentText(_translate("Dialog", "x"))
        self.display_resolution_combobox.setItemText(0, _translate("Dialog", "xxx"))
        self.display_resolution_combobox.setItemText(1, _translate("Dialog", "xx"))
        self.display_resolution_combobox.setItemText(2, _translate("Dialog", "x"))
        self.display_resolution_combobox.setItemText(3, _translate("Dialog", "x.0"))
        self.display_resolution_combobox.setItemText(4, _translate("Dialog", "x.00"))
        self.display_resolution_combobox.setItemText(5, _translate("Dialog", "x.000"))
        self.display_resolution_combobox.setItemText(6, _translate("Dialog", "x.0000"))
        self.display_resolution_combobox.setItemText(7, _translate("Dialog", "x.0000"))
        self.auto_calc_points_checkbox.setTitle(_translate("Dialog", "Рассчитать точки поверки"))
        self.edit_frequency_button.setText(_translate("Dialog", "..."))
        self.start_point_down_radio.setText(_translate("Dialog", "Снизу"))
        self.start_point_up_radio.setText(_translate("Dialog", "Сверху"))
        self.label_9.setText(_translate("Dialog", "Частота, Гц"))
        self.step_edit.setText(_translate("Dialog", "0"))
        self.label_6.setText(_translate("Dialog", "Шаг поверки"))
        self.step_help_button.setText(_translate("Dialog", "?"))
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
