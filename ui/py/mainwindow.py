# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        MainWindow.setAnimated(True)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menuBar.setObjectName("menuBar")
        self.options_menu = QtWidgets.QMenu(self.menuBar)
        self.options_menu.setObjectName("options_menu")
        self.window_menu = QtWidgets.QMenu(self.menuBar)
        self.window_menu.setObjectName("window_menu")
        MainWindow.setMenuBar(self.menuBar)
        self.back_action = QtWidgets.QAction(MainWindow)
        self.back_action.setObjectName("back_action")
        self.change_fixed_range_action = QtWidgets.QAction(MainWindow)
        self.change_fixed_range_action.setObjectName("change_fixed_range_action")
        self.options_menu.addAction(self.change_fixed_range_action)
        self.window_menu.addAction(self.back_action)
        self.menuBar.addAction(self.options_menu.menuAction())
        self.menuBar.addAction(self.window_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.options_menu.setTitle(_translate("MainWindow", "Опции"))
        self.window_menu.setTitle(_translate("MainWindow", "Окно"))
        self.back_action.setText(_translate("MainWindow", "Назад"))
        self.change_fixed_range_action.setText(_translate("MainWindow", "Изменить фиксированный шаг"))
