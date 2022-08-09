# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_scales_tabwidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_template_scales_tabwidget(object):
    def setupUi(self, template_scales_tabwidget):
        template_scales_tabwidget.setObjectName("template_scales_tabwidget")
        template_scales_tabwidget.resize(231, 284)
        font = QtGui.QFont()
        font.setPointSize(10)
        template_scales_tabwidget.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(template_scales_tabwidget)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(template_scales_tabwidget)
        self.tabWidget.setStyleSheet("QTabBar::tab::last\n"
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
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(template_scales_tabwidget)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(template_scales_tabwidget)

    def retranslateUi(self, template_scales_tabwidget):
        _translate = QtCore.QCoreApplication.translate
        template_scales_tabwidget.setWindowTitle(_translate("template_scales_tabwidget", "Form"))
