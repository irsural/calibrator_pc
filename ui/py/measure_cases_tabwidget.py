# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'measure_cases_tabwidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_measure_cases_tabwidget_2(object):
    def setupUi(self, measure_cases_tabwidget_2):
        measure_cases_tabwidget_2.setObjectName("measure_cases_tabwidget_2")
        measure_cases_tabwidget_2.resize(310, 304)
        font = QtGui.QFont()
        font.setPointSize(10)
        measure_cases_tabwidget_2.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(measure_cases_tabwidget_2)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.measure_cases_tabwidget = QtWidgets.QTabWidget(measure_cases_tabwidget_2)
        self.measure_cases_tabwidget.setStyleSheet("QTabBar::tab::last\n"
"{\n"
"    margin-right: 2px;\n"
"    margin-left:0px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    margin-left: 10px;\n"
"    margin-right: 10px;\n"
"    margin-bottom: 10px;\n"
"}")
        self.measure_cases_tabwidget.setDocumentMode(False)
        self.measure_cases_tabwidget.setTabsClosable(True)
        self.measure_cases_tabwidget.setTabBarAutoHide(False)
        self.measure_cases_tabwidget.setObjectName("measure_cases_tabwidget")
        self.verticalLayout.addWidget(self.measure_cases_tabwidget)

        self.retranslateUi(measure_cases_tabwidget_2)
        self.measure_cases_tabwidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(measure_cases_tabwidget_2)

    def retranslateUi(self, measure_cases_tabwidget_2):
        _translate = QtCore.QCoreApplication.translate
        measure_cases_tabwidget_2.setWindowTitle(_translate("measure_cases_tabwidget_2", "Form"))
