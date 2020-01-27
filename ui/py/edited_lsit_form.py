# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/edited_lsit_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(255, 288)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lsitname_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lsitname_label.setFont(font)
        self.lsitname_label.setObjectName("lsitname_label")
        self.horizontalLayout_2.addWidget(self.lsitname_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.add_list_item_button = QtWidgets.QPushButton(Dialog)
        self.add_list_item_button.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.add_list_item_button.setFont(font)
        self.add_list_item_button.setObjectName("add_list_item_button")
        self.horizontalLayout_2.addWidget(self.add_list_item_button)
        self.delete_list_item_button = QtWidgets.QPushButton(Dialog)
        self.delete_list_item_button.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.delete_list_item_button.setFont(font)
        self.delete_list_item_button.setObjectName("delete_list_item_button")
        self.horizontalLayout_2.addWidget(self.delete_list_item_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.list_widget = QtWidgets.QListWidget(Dialog)
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
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.accept_button = QtWidgets.QPushButton(Dialog)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout.addWidget(self.accept_button)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lsitname_label.setText(_translate("Dialog", "List name"))
        self.add_list_item_button.setText(_translate("Dialog", "+"))
        self.delete_list_item_button.setText(_translate("Dialog", "-"))
        self.list_widget.setSortingEnabled(False)
        self.accept_button.setText(_translate("Dialog", "Принять"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
