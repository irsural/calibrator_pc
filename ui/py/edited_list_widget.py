# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/edited_list_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(242, 288)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lsitname_label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lsitname_label.setFont(font)
        self.lsitname_label.setObjectName("lsitname_label")
        self.horizontalLayout_2.addWidget(self.lsitname_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.add_list_item_button = QtWidgets.QPushButton(Form)
        self.add_list_item_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.add_list_item_button.setFont(font)
        self.add_list_item_button.setObjectName("add_list_item_button")
        self.horizontalLayout_2.addWidget(self.add_list_item_button)
        self.delete_list_item_button = QtWidgets.QPushButton(Form)
        self.delete_list_item_button.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.delete_list_item_button.setFont(font)
        self.delete_list_item_button.setObjectName("delete_list_item_button")
        self.horizontalLayout_2.addWidget(self.delete_list_item_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.list_widget = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.list_widget.setFont(font)
        self.list_widget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.list_widget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setMovement(QtWidgets.QListView.Free)
        self.list_widget.setFlow(QtWidgets.QListView.TopToBottom)
        self.list_widget.setProperty("isWrapping", False)
        self.list_widget.setResizeMode(QtWidgets.QListView.Fixed)
        self.list_widget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.list_widget.setViewMode(QtWidgets.QListView.ListMode)
        self.list_widget.setModelColumn(0)
        self.list_widget.setUniformItemSizes(False)
        self.list_widget.setSelectionRectVisible(False)
        self.list_widget.setObjectName("list_widget")
        self.verticalLayout.addWidget(self.list_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.add_list_item_button, self.delete_list_item_button)
        Form.setTabOrder(self.delete_list_item_button, self.list_widget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lsitname_label.setText(_translate("Form", "List name"))
        self.add_list_item_button.setText(_translate("Form", "+"))
        self.delete_list_item_button.setText(_translate("Form", "-"))
        self.list_widget.setSortingEnabled(False)
