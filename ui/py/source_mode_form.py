# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/source_mode_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(362, 328)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.clb_state_label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clb_state_label.sizePolicy().hasHeightForWidth())
        self.clb_state_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.clb_state_label.setFont(font)
        self.clb_state_label.setScaledContents(False)
        self.clb_state_label.setObjectName("clb_state_label")
        self.horizontalLayout_4.addWidget(self.clb_state_label)
        self.verticalLayout_2.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.clb_list_combobox = QtWidgets.QComboBox(Form)
        self.clb_list_combobox.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.clb_list_combobox.setFont(font)
        self.clb_list_combobox.setObjectName("clb_list_combobox")
        self.horizontalLayout_2.addWidget(self.clb_list_combobox)
        self.aci_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.aci_radio.setFont(font)
        self.aci_radio.setChecked(True)
        self.aci_radio.setObjectName("aci_radio")
        self.signal_group = QtWidgets.QButtonGroup(Form)
        self.signal_group.setObjectName("signal_group")
        self.signal_group.addButton(self.aci_radio)
        self.horizontalLayout_2.addWidget(self.aci_radio)
        self.acv_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.acv_radio.setFont(font)
        self.acv_radio.setChecked(False)
        self.acv_radio.setObjectName("acv_radio")
        self.signal_group.addButton(self.acv_radio)
        self.horizontalLayout_2.addWidget(self.acv_radio)
        self.dci_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dci_radio.setFont(font)
        self.dci_radio.setObjectName("dci_radio")
        self.signal_group.addButton(self.dci_radio)
        self.horizontalLayout_2.addWidget(self.dci_radio)
        self.dcv_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dcv_radio.setFont(font)
        self.dcv_radio.setObjectName("dcv_radio")
        self.signal_group.addButton(self.dcv_radio)
        self.horizontalLayout_2.addWidget(self.dcv_radio)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.apply_frequency_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apply_frequency_button.sizePolicy().hasHeightForWidth())
        self.apply_frequency_button.setSizePolicy(sizePolicy)
        self.apply_frequency_button.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.apply_frequency_button.setFont(font)
        self.apply_frequency_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.apply_frequency_button.setIcon(icon)
        self.apply_frequency_button.setIconSize(QtCore.QSize(35, 35))
        self.apply_frequency_button.setObjectName("apply_frequency_button")
        self.gridLayout.addWidget(self.apply_frequency_button, 5, 1, 1, 1)
        self.apply_amplitude_button = QtWidgets.QPushButton(Form)
        self.apply_amplitude_button.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.apply_amplitude_button.setFont(font)
        self.apply_amplitude_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/ok.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.apply_amplitude_button.setIcon(icon1)
        self.apply_amplitude_button.setIconSize(QtCore.QSize(35, 35))
        self.apply_amplitude_button.setFlat(False)
        self.apply_amplitude_button.setObjectName("apply_amplitude_button")
        self.gridLayout.addWidget(self.apply_amplitude_button, 3, 1, 1, 1)
        self.frequency_edit = QEditCopyButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frequency_edit.sizePolicy().hasHeightForWidth())
        self.frequency_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.frequency_edit.setFont(font)
        self.frequency_edit.setObjectName("frequency_edit")
        self.gridLayout.addWidget(self.frequency_edit, 5, 0, 1, 1)
        self.amplitude_edit = QEditCopyButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amplitude_edit.sizePolicy().hasHeightForWidth())
        self.amplitude_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.amplitude_edit.setFont(font)
        self.amplitude_edit.setStyleSheet("")
        self.amplitude_edit.setObjectName("amplitude_edit")
        self.gridLayout.addWidget(self.amplitude_edit, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.source_mode_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.source_mode_radio.setFont(font)
        self.source_mode_radio.setChecked(True)
        self.source_mode_radio.setObjectName("source_mode_radio")
        self.mode_group = QtWidgets.QButtonGroup(Form)
        self.mode_group.setObjectName("mode_group")
        self.mode_group.addButton(self.source_mode_radio)
        self.horizontalLayout_5.addWidget(self.source_mode_radio)
        self.fixed_mode_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fixed_mode_radio.setFont(font)
        self.fixed_mode_radio.setObjectName("fixed_mode_radio")
        self.mode_group.addButton(self.fixed_mode_radio)
        self.horizontalLayout_5.addWidget(self.fixed_mode_radio)
        self.detuning_radio = QtWidgets.QRadioButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.detuning_radio.setFont(font)
        self.detuning_radio.setObjectName("detuning_radio")
        self.mode_group.addButton(self.detuning_radio)
        self.horizontalLayout_5.addWidget(self.detuning_radio)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.enable_button = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.enable_button.setFont(font)
        self.enable_button.setIconSize(QtCore.QSize(25, 25))
        self.enable_button.setCheckable(True)
        self.enable_button.setObjectName("enable_button")
        self.verticalLayout_2.addWidget(self.enable_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.aci_radio, self.acv_radio)
        Form.setTabOrder(self.acv_radio, self.dci_radio)
        Form.setTabOrder(self.dci_radio, self.dcv_radio)
        Form.setTabOrder(self.dcv_radio, self.source_mode_radio)
        Form.setTabOrder(self.source_mode_radio, self.fixed_mode_radio)
        Form.setTabOrder(self.fixed_mode_radio, self.detuning_radio)
        Form.setTabOrder(self.detuning_radio, self.enable_button)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Режим источника"))
        self.label_4.setText(_translate("Form", "Статус:"))
        self.clb_state_label.setText(_translate("Form", "Остановлен"))
        self.aci_radio.setText(_translate("Form", "I~"))
        self.acv_radio.setText(_translate("Form", "U~"))
        self.dci_radio.setText(_translate("Form", "I="))
        self.dcv_radio.setText(_translate("Form", "U="))
        self.frequency_edit.setText(_translate("Form", "0"))
        self.amplitude_edit.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "Частота, Гц"))
        self.label_5.setText(_translate("Form", "Амплитуда"))
        self.source_mode_radio.setText(_translate("Form", "Источник"))
        self.fixed_mode_radio.setText(_translate("Form", "Фиксир."))
        self.detuning_radio.setText(_translate("Form", "Расстройка"))
        self.enable_button.setText(_translate("Form", "Старт"))
from custom_widgets.CustomLineEdit import QEditCopyButton
import icons_rc
