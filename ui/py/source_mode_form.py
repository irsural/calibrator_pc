# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source_mode_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_source_mode_dialog(object):
    def setupUi(self, source_mode_dialog):
        source_mode_dialog.setObjectName("source_mode_dialog")
        source_mode_dialog.resize(451, 398)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(source_mode_dialog.sizePolicy().hasHeightForWidth())
        source_mode_dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(source_mode_dialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(source_mode_dialog)
        QtCore.QMetaObject.connectSlotsByName(source_mode_dialog)

    def retranslateUi(self, source_mode_dialog):
        _translate = QtCore.QCoreApplication.translate
        source_mode_dialog.setWindowTitle(_translate("source_mode_dialog", "Режим источника"))
import icons
