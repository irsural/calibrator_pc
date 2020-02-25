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
        Form.resize(469, 49)
        font = QtGui.QFont()
        font.setPointSize(13)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.source_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.source_mode_button.sizePolicy().hasHeightForWidth())
        self.source_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.source_mode_button.setFont(font)
        self.source_mode_button.setObjectName("source_mode_button")
        self.horizontalLayout.addWidget(self.source_mode_button)
        self.no_template_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_template_mode_button.sizePolicy().hasHeightForWidth())
        self.no_template_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.no_template_mode_button.setFont(font)
        self.no_template_mode_button.setObjectName("no_template_mode_button")
        self.horizontalLayout.addWidget(self.no_template_mode_button)
        self.template_mode_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.template_mode_button.sizePolicy().hasHeightForWidth())
        self.template_mode_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.template_mode_button.setFont(font)
        self.template_mode_button.setObjectName("template_mode_button")
        self.horizontalLayout.addWidget(self.template_mode_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.source_mode_button.setText(_translate("Form", "Режим источника"))
        self.no_template_mode_button.setText(_translate("Form", "Быстрая поверка"))
        self.template_mode_button.setText(_translate("Form", "Шаблоны поверки"))
