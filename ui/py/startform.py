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
        Form.resize(688, 312)
        font = QtGui.QFont()
        font.setPointSize(13)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.template_mode_button_2 = QtWidgets.QToolButton(Form)
        self.template_mode_button_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.template_mode_button_2.sizePolicy().hasHeightForWidth())
        self.template_mode_button_2.setSizePolicy(sizePolicy)
        self.template_mode_button_2.setMinimumSize(QtCore.QSize(100, 0))
        self.template_mode_button_2.setAutoRaise(True)
        self.template_mode_button_2.setArrowType(QtCore.Qt.NoArrow)
        self.template_mode_button_2.setObjectName("template_mode_button_2")
        self.horizontalLayout.addWidget(self.template_mode_button_2)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.source_mode_button = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.source_mode_button.sizePolicy().hasHeightForWidth())
        self.source_mode_button.setSizePolicy(sizePolicy)
        self.source_mode_button.setMinimumSize(QtCore.QSize(100, 0))
        self.source_mode_button.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.source_mode_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.source_mode_button.setAutoRaise(True)
        self.source_mode_button.setObjectName("source_mode_button")
        self.horizontalLayout.addWidget(self.source_mode_button)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.no_template_mode_button = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_template_mode_button.sizePolicy().hasHeightForWidth())
        self.no_template_mode_button.setSizePolicy(sizePolicy)
        self.no_template_mode_button.setMinimumSize(QtCore.QSize(100, 0))
        self.no_template_mode_button.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.no_template_mode_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.no_template_mode_button.setAutoRaise(True)
        self.no_template_mode_button.setObjectName("no_template_mode_button")
        self.horizontalLayout.addWidget(self.no_template_mode_button)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.template_mode_button = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.template_mode_button.sizePolicy().hasHeightForWidth())
        self.template_mode_button.setSizePolicy(sizePolicy)
        self.template_mode_button.setMinimumSize(QtCore.QSize(100, 0))
        self.template_mode_button.setAutoRaise(True)
        self.template_mode_button.setArrowType(QtCore.Qt.NoArrow)
        self.template_mode_button.setObjectName("template_mode_button")
        self.horizontalLayout.addWidget(self.template_mode_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.measures_table = QtWidgets.QTableView(Form)
        self.measures_table.setStyleSheet("")
        self.measures_table.setDragEnabled(False)
        self.measures_table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.measures_table.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.measures_table.setAlternatingRowColors(True)
        self.measures_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.measures_table.setWordWrap(True)
        self.measures_table.setObjectName("measures_table")
        self.measures_table.horizontalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.measures_table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Последние измерения"))
        self.template_mode_button_2.setText(_translate("Form", "Создать\n"
"отчет"))
        self.source_mode_button.setText(_translate("Form", "Режим\n"
"источника"))
        self.no_template_mode_button.setText(_translate("Form", "Быстрая\n"
"поверка"))
        self.template_mode_button.setText(_translate("Form", "Шаблоны\n"
"поверки"))
