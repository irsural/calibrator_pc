# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
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
        self.settings_menu = QtWidgets.QMenu(self.menuBar)
        self.settings_menu.setObjectName("settings_menu")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.change_fixed_range_action = QtWidgets.QAction(MainWindow)
        self.change_fixed_range_action.setObjectName("change_fixed_range_action")
        self.enter_settings_action = QtWidgets.QAction(MainWindow)
        self.enter_settings_action.setObjectName("enter_settings_action")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.settings_menu.addAction(self.enter_settings_action)
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.settings_menu.menuAction())
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.settings_menu.setTitle(_translate("MainWindow", "Настройки"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.change_fixed_range_action.setText(_translate("MainWindow", "Изменить фиксированный шаг"))
        self.enter_settings_action.setText(_translate("MainWindow", "Настройки..."))
        self.action.setText(_translate("MainWindow", "О программе"))
