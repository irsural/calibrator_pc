# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/startform.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(370, 261)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.source_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.source_mode_button.sizePolicy().hasHeightForWidth())
        self.source_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.source_mode_button.setFont(font)
        self.source_mode_button.setObjectName("source_mode_button")
        self.verticalLayout.addWidget(self.source_mode_button)
        self.no_template_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_template_mode_button.sizePolicy().hasHeightForWidth())
        self.no_template_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.no_template_mode_button.setFont(font)
        self.no_template_mode_button.setObjectName("no_template_mode_button")
        self.verticalLayout.addWidget(self.no_template_mode_button)
        self.template_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.template_mode_button.sizePolicy().hasHeightForWidth())
        self.template_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.template_mode_button.setFont(font)
        self.template_mode_button.setObjectName("template_mode_button")
        self.verticalLayout.addWidget(self.template_mode_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.source_mode_button.setText(_translate("Form", "Режим источника"))
        self.no_template_mode_button.setText(_translate("Form", "Поверка без шаблона"))
        self.template_mode_button.setText(_translate("Form", "Поверка с шаблоном"))
