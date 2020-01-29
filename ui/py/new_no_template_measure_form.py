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
        Dialog.resize(338, 462)
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
        self.params_grid = QtWidgets.QGridLayout()
        self.params_grid.setObjectName("params_grid")
        self.clb_list_combobox = QtWidgets.QComboBox(Dialog)
        self.clb_list_combobox.setMinimumSize(QtCore.QSize(0, 0))
        self.clb_list_combobox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clb_list_combobox.setFont(font)
        self.clb_list_combobox.setObjectName("clb_list_combobox")
        self.params_grid.addWidget(self.clb_list_combobox, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.params_grid.addWidget(self.label_4, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.params_grid.addWidget(self.label_5, 2, 0, 1, 1)
        self.accuracy_class_spinbox = QtWidgets.QDoubleSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accuracy_class_spinbox.setFont(font)
        self.accuracy_class_spinbox.setDecimals(4)
        self.accuracy_class_spinbox.setMinimum(0.0001)
        self.accuracy_class_spinbox.setMaximum(10.0)
        self.accuracy_class_spinbox.setSingleStep(0.05)
        self.accuracy_class_spinbox.setProperty("value", 0.05)
        self.accuracy_class_spinbox.setObjectName("accuracy_class_spinbox")
        self.params_grid.addWidget(self.accuracy_class_spinbox, 3, 0, 1, 1)
        self.minimal_discrete = QEditDoubleClick(Dialog)
        self.minimal_discrete.setMinimumSize(QtCore.QSize(0, 0))
        self.minimal_discrete.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.minimal_discrete.setFont(font)
        self.minimal_discrete.setObjectName("minimal_discrete")
        self.params_grid.addWidget(self.minimal_discrete, 3, 1, 1, 1)
        self.upper_bound_edit = QEditDoubleClick(Dialog)
        self.upper_bound_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.upper_bound_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.upper_bound_edit.setFont(font)
        self.upper_bound_edit.setObjectName("upper_bound_edit")
        self.params_grid.addWidget(self.upper_bound_edit, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.params_grid.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setMinimumSize(QtCore.QSize(156, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.params_grid.addWidget(self.label_11, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.params_grid.addWidget(self.label_10, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.params_grid.addWidget(self.label_7, 4, 0, 1, 1)
        self.comment_edit = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comment_edit.setFont(font)
        self.comment_edit.setObjectName("comment_edit")
        self.params_grid.addWidget(self.comment_edit, 5, 1, 1, 1)
        self.start_deviation_spinbox = QtWidgets.QSpinBox(Dialog)
        self.start_deviation_spinbox.setMinimumSize(QtCore.QSize(0, 0))
        self.start_deviation_spinbox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_deviation_spinbox.setFont(font)
        self.start_deviation_spinbox.setMinimum(1)
        self.start_deviation_spinbox.setMaximum(50)
        self.start_deviation_spinbox.setProperty("value", 10)
        self.start_deviation_spinbox.setObjectName("start_deviation_spinbox")
        self.params_grid.addWidget(self.start_deviation_spinbox, 5, 0, 1, 1)
        self.verticalLayout.addLayout(self.params_grid)
        self.auto_calc_points_checkbox = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auto_calc_points_checkbox.setFont(font)
        self.auto_calc_points_checkbox.setFlat(True)
        self.auto_calc_points_checkbox.setCheckable(True)
        self.auto_calc_points_checkbox.setChecked(False)
        self.auto_calc_points_checkbox.setObjectName("auto_calc_points_checkbox")
        self.gridLayout = QtWidgets.QGridLayout(self.auto_calc_points_checkbox)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.lower_bound_edit = QEditDoubleClick(self.auto_calc_points_checkbox)
        self.lower_bound_edit.setMinimumSize(QtCore.QSize(0, 0))
        self.lower_bound_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lower_bound_edit.setFont(font)
        self.lower_bound_edit.setObjectName("lower_bound_edit")
        self.gridLayout.addWidget(self.lower_bound_edit, 1, 0, 1, 1)
        self.step_edit = QEditDoubleClick(self.auto_calc_points_checkbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_edit.sizePolicy().hasHeightForWidth())
        self.step_edit.setSizePolicy(sizePolicy)
        self.step_edit.setMinimumSize(QtCore.QSize(156, 0))
        self.step_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.step_edit.setFont(font)
        self.step_edit.setObjectName("step_edit")
        self.gridLayout.addWidget(self.step_edit, 1, 1, 1, 1)
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
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.auto_calc_points_checkbox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
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
        self.edit_frequency_button.setAutoDefault(False)
        self.edit_frequency_button.setObjectName("edit_frequency_button")
        self.horizontalLayout_2.addWidget(self.edit_frequency_button)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)
        self.verticalLayout.addWidget(self.auto_calc_points_checkbox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
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
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Измерение без шаблона"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p>Режим<span style=\" color:#ff0000;\">*</span></p></body></html>"))
        self.aci_radio.setText(_translate("Dialog", "I~"))
        self.acv_radio.setText(_translate("Dialog", "U~"))
        self.dci_radio.setText(_translate("Dialog", "I="))
        self.dcv_radio.setText(_translate("Dialog", "U="))
        self.label_2.setText(_translate("Dialog", "Параметры поверки"))
        self.label_4.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Влияет на определение поверяемой точки.</p><p>Например, если минимальный дискрет установлен 10 мВ, а измеренное значение равно 33 мВ, поверяемая точка будет определена, как 30 мВ.</p><p>А если минимальный дискрет установлен 20 мВ, а измеренное значение равно 33 мВ, поверяемая точка будет определена, как 40 мВ.</p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>Минимальный дискрет<span style=\" color:#ff0000;\">*</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>Класс точности<span style=\" color:#ff0000;\">*</span></p></body></html>"))
        self.minimal_discrete.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Влияет на определение поверяемой точки.</p><p>Например, если минимальный дискрет установлен 10 мВ, а измеренное значение равно 33 мВ, поверяемая точка будет определена, как 30 мВ.</p><p>А если минимальный дискрет установлен 20 мВ, а измеренное значение равно 33 мВ, поверяемая точка будет определена, как 40 мВ.</p></body></html>"))
        self.minimal_discrete.setText(_translate("Dialog", "0"))
        self.upper_bound_edit.setText(_translate("Dialog", "0"))
        self.label_8.setText(_translate("Dialog", "<html><head/><body><p>Калибратор<span style=\" color:#ff0000;\">*</span></p></body></html>"))
        self.label_11.setText(_translate("Dialog", "Комментарий"))
        self.label_10.setText(_translate("Dialog", "<html><head/><body><p>Максимальная точка<span style=\" color:#ff0000;\">*</span></p></body></html>"))
        self.label_7.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Определяет отклонение при переходе к выбранной точке.</p><p>Например, при установленном отклонении 10%, при переходе к точке 600 В будет установлено напряжение 540 В.</p><p>Отклонение рассчитывается в процентах от максимальной точки.</p></body></html>"))
        self.label_7.setText(_translate("Dialog", "Начальное отклонение, %"))
        self.start_deviation_spinbox.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Определяет отклонение при переходе к выбранной точке.</p><p>Например, при установленном отклонении 10%, при переходе к точке 600 В будет установлено напряжение 540 В.</p><p>Отклонение рассчитывается в процентах от максимальной точки.</p></body></html>"))
        self.auto_calc_points_checkbox.setTitle(_translate("Dialog", "Рассчитать точки поверки"))
        self.label_3.setText(_translate("Dialog", "Минимальная точка"))
        self.label_6.setText(_translate("Dialog", "Шаг поверки"))
        self.lower_bound_edit.setText(_translate("Dialog", "0"))
        self.step_edit.setText(_translate("Dialog", "0"))
        self.start_point_down_radio.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Параметры &quot;Снизу&quot; и &quot;Сверху&quot; определяют начальную точку, от которой будут рассчитываться точки с интервалом &quot;Шаг поверки&quot; (От минимальной или от максимальной точки).</p><p>Для приборов с равномерной шкалой не имеет значения.</p></body></html>"))
        self.start_point_down_radio.setText(_translate("Dialog", "Снизу"))
        self.start_point_up_radio.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Параметры &quot;Снизу&quot; и &quot;Сверху&quot; определяют начальную точку, от которой будут рассчитываться точки с интервалом &quot;Шаг поверки&quot; (От минимальной или от максимальной точки).</p><p>Для приборов с равномерной шкалой не имеет значения.</p></body></html>"))
        self.start_point_up_radio.setText(_translate("Dialog", "Сверху"))
        self.label_9.setText(_translate("Dialog", "Частота, Гц"))
        self.edit_frequency_button.setText(_translate("Dialog", "..."))
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
from custom_widgets.CustomLineEdit import QEditDoubleClick
