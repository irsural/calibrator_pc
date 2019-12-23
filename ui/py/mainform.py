# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/mainform.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(313, 247)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.clb_list_combobox = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.clb_list_combobox.setFont(font)
        self.clb_list_combobox.setObjectName("clb_list_combobox")
        self.horizontalLayout_3.addWidget(self.clb_list_combobox)
        self.usb_state_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.usb_state_label.setFont(font)
        self.usb_state_label.setObjectName("usb_state_label")
        self.horizontalLayout_3.addWidget(self.usb_state_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.amplitude_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.amplitude_label.setFont(font)
        self.amplitude_label.setObjectName("amplitude_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.amplitude_label)
        self.amplitude_spinbox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.amplitude_spinbox.setFont(font)
        self.amplitude_spinbox.setMaximum(600.0)
        self.amplitude_spinbox.setObjectName("amplitude_spinbox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.amplitude_spinbox)
        self.frequency_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.frequency_label.setFont(font)
        self.frequency_label.setObjectName("frequency_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.frequency_label)
        self.frequency_spinbox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.frequency_spinbox.setFont(font)
        self.frequency_spinbox.setObjectName("frequency_spinbox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.frequency_spinbox)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.acv_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.acv_radio.setFont(font)
        self.acv_radio.setObjectName("acv_radio")
        self.horizontalLayout_2.addWidget(self.acv_radio)
        self.dcv_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dcv_radio.setFont(font)
        self.dcv_radio.setObjectName("dcv_radio")
        self.horizontalLayout_2.addWidget(self.dcv_radio)
        self.aci_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.aci_radio.setFont(font)
        self.aci_radio.setObjectName("aci_radio")
        self.horizontalLayout_2.addWidget(self.aci_radio)
        self.dci_radio = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dci_radio.setFont(font)
        self.dci_radio.setObjectName("dci_radio")
        self.horizontalLayout_2.addWidget(self.dci_radio)
        self.polarity_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.polarity_button.setFont(font)
        self.polarity_button.setCheckable(True)
        self.polarity_button.setObjectName("polarity_button")
        self.horizontalLayout_2.addWidget(self.polarity_button)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.enable_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.enable_button.setFont(font)
        self.enable_button.setCheckable(True)
        self.enable_button.setObjectName("enable_button")
        self.gridLayout.addWidget(self.enable_button, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 313, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.usb_state_label.setText(_translate("MainWindow", "Отключено"))
        self.amplitude_label.setText(_translate("MainWindow", "Амплитуда"))
        self.frequency_label.setText(_translate("MainWindow", "Частота"))
        self.acv_radio.setText(_translate("MainWindow", "~U"))
        self.dcv_radio.setText(_translate("MainWindow", "=U"))
        self.aci_radio.setText(_translate("MainWindow", "~I"))
        self.dci_radio.setText(_translate("MainWindow", "=I"))
        self.polarity_button.setText(_translate("MainWindow", "+"))
        self.enable_button.setText(_translate("MainWindow", "Enable"))
