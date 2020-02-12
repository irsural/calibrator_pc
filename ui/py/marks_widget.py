# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/marks_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_marks_widget(object):
    def setupUi(self, marks_widget):
        marks_widget.setObjectName("marks_widget")
        marks_widget.resize(365, 300)
        font = QtGui.QFont()
        font.setPointSize(10)
        marks_widget.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(marks_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.marks_table = QtWidgets.QTableWidget(marks_widget)
        self.marks_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.marks_table.setObjectName("marks_table")
        self.marks_table.setColumnCount(3)
        self.marks_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.marks_table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.marks_table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_mark_button = QtWidgets.QPushButton(marks_widget)
        self.add_mark_button.setMaximumSize(QtCore.QSize(35, 16777215))
        self.add_mark_button.setObjectName("add_mark_button")
        self.verticalLayout.addWidget(self.add_mark_button)
        self.delete_mark_button = QtWidgets.QPushButton(marks_widget)
        self.delete_mark_button.setMaximumSize(QtCore.QSize(35, 16777215))
        self.delete_mark_button.setObjectName("delete_mark_button")
        self.verticalLayout.addWidget(self.delete_mark_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(marks_widget)
        QtCore.QMetaObject.connectSlotsByName(marks_widget)

    def retranslateUi(self, marks_widget):
        _translate = QtCore.QCoreApplication.translate
        marks_widget.setWindowTitle(_translate("marks_widget", "Form"))
        item = self.marks_table.horizontalHeaderItem(0)
        item.setText(_translate("marks_widget", "Параметр"))
        item = self.marks_table.horizontalHeaderItem(1)
        item.setText(_translate("marks_widget", "Тэг"))
        item = self.marks_table.horizontalHeaderItem(2)
        item.setText(_translate("marks_widget", "Значение\n"
"по умолчанию"))
        self.add_mark_button.setText(_translate("marks_widget", "+"))
        self.delete_mark_button.setText(_translate("marks_widget", "-"))
