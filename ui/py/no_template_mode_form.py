# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/no_template_mode_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(813, 495)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.usb_state_label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.usb_state_label.setFont(font)
        self.usb_state_label.setObjectName("usb_state_label")
        self.horizontalLayout_3.addWidget(self.usb_state_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.clb_state_label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.clb_state_label.setFont(font)
        self.clb_state_label.setObjectName("clb_state_label")
        self.horizontalLayout_3.addWidget(self.clb_state_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.frame)
        self.splitter_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitter_2.setLineWidth(1)
        self.splitter_2.setMidLineWidth(5)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setHandleWidth(5)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.groupBox = QtWidgets.QGroupBox(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.groupBox)
        self.frame_2.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_2.setFont(font)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.label_2.setMouseTracking(False)
        self.label_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.rough_plus_button = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rough_plus_button.sizePolicy().hasHeightForWidth())
        self.rough_plus_button.setSizePolicy(sizePolicy)
        self.rough_plus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.rough_plus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.rough_plus_button.setFont(font)
        self.rough_plus_button.setAutoRepeat(True)
        self.rough_plus_button.setAutoRepeatDelay(600)
        self.rough_plus_button.setAutoRepeatInterval(10)
        self.rough_plus_button.setObjectName("rough_plus_button")
        self.verticalLayout_7.addWidget(self.rough_plus_button)
        self.rough_minus_button = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rough_minus_button.sizePolicy().hasHeightForWidth())
        self.rough_minus_button.setSizePolicy(sizePolicy)
        self.rough_minus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.rough_minus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.rough_minus_button.setFont(font)
        self.rough_minus_button.setAutoRepeat(True)
        self.rough_minus_button.setAutoRepeatDelay(600)
        self.rough_minus_button.setAutoRepeatInterval(10)
        self.rough_minus_button.setObjectName("rough_minus_button")
        self.verticalLayout_7.addWidget(self.rough_minus_button)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_5 = QtWidgets.QFrame(self.groupBox)
        self.frame_5.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_5.setFont(font)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_10.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(True)
        font.setKerning(True)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.label_8.setObjectName("label_8")
        self.verticalLayout_10.addWidget(self.label_8)
        self.common_plus_button = QtWidgets.QPushButton(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.common_plus_button.sizePolicy().hasHeightForWidth())
        self.common_plus_button.setSizePolicy(sizePolicy)
        self.common_plus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.common_plus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.common_plus_button.setFont(font)
        self.common_plus_button.setAutoRepeat(True)
        self.common_plus_button.setAutoRepeatDelay(600)
        self.common_plus_button.setAutoRepeatInterval(10)
        self.common_plus_button.setObjectName("common_plus_button")
        self.verticalLayout_10.addWidget(self.common_plus_button)
        self.common_minus_button = QtWidgets.QPushButton(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.common_minus_button.sizePolicy().hasHeightForWidth())
        self.common_minus_button.setSizePolicy(sizePolicy)
        self.common_minus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.common_minus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.common_minus_button.setFont(font)
        self.common_minus_button.setAutoRepeat(True)
        self.common_minus_button.setAutoRepeatDelay(600)
        self.common_minus_button.setAutoRepeatInterval(10)
        self.common_minus_button.setObjectName("common_minus_button")
        self.verticalLayout_10.addWidget(self.common_minus_button)
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.frame_4 = QtWidgets.QFrame(self.groupBox)
        self.frame_4.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_4.setFont(font)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_8.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.exact_plus_button = QtWidgets.QPushButton(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exact_plus_button.sizePolicy().hasHeightForWidth())
        self.exact_plus_button.setSizePolicy(sizePolicy)
        self.exact_plus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.exact_plus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.exact_plus_button.setFont(font)
        self.exact_plus_button.setAutoRepeat(True)
        self.exact_plus_button.setAutoRepeatDelay(600)
        self.exact_plus_button.setAutoRepeatInterval(10)
        self.exact_plus_button.setObjectName("exact_plus_button")
        self.verticalLayout_8.addWidget(self.exact_plus_button)
        self.exact_minus_button = QtWidgets.QPushButton(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exact_minus_button.sizePolicy().hasHeightForWidth())
        self.exact_minus_button.setSizePolicy(sizePolicy)
        self.exact_minus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.exact_minus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.exact_minus_button.setFont(font)
        self.exact_minus_button.setAutoRepeat(True)
        self.exact_minus_button.setAutoRepeatDelay(600)
        self.exact_minus_button.setAutoRepeatInterval(10)
        self.exact_minus_button.setObjectName("exact_minus_button")
        self.verticalLayout_8.addWidget(self.exact_minus_button)
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.frame_6 = QtWidgets.QFrame(self.groupBox)
        self.frame_6.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_6.setFont(font)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_9.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.fixed_step_combobox = QtWidgets.QComboBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_step_combobox.sizePolicy().hasHeightForWidth())
        self.fixed_step_combobox.setSizePolicy(sizePolicy)
        self.fixed_step_combobox.setMaximumSize(QtCore.QSize(16777215, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(True)
        self.fixed_step_combobox.setFont(font)
        self.fixed_step_combobox.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.fixed_step_combobox.setEditable(False)
        self.fixed_step_combobox.setModelColumn(0)
        self.fixed_step_combobox.setObjectName("fixed_step_combobox")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.fixed_step_combobox.addItem("")
        self.verticalLayout_9.addWidget(self.fixed_step_combobox)
        self.fixed_plus_button = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_plus_button.sizePolicy().hasHeightForWidth())
        self.fixed_plus_button.setSizePolicy(sizePolicy)
        self.fixed_plus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.fixed_plus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.fixed_plus_button.setFont(font)
        self.fixed_plus_button.setAutoRepeat(True)
        self.fixed_plus_button.setAutoRepeatDelay(600)
        self.fixed_plus_button.setAutoRepeatInterval(10)
        self.fixed_plus_button.setObjectName("fixed_plus_button")
        self.verticalLayout_9.addWidget(self.fixed_plus_button)
        self.fixed_minus_button = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_minus_button.sizePolicy().hasHeightForWidth())
        self.fixed_minus_button.setSizePolicy(sizePolicy)
        self.fixed_minus_button.setMinimumSize(QtCore.QSize(0, 0))
        self.fixed_minus_button.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.fixed_minus_button.setFont(font)
        self.fixed_minus_button.setAutoRepeat(True)
        self.fixed_minus_button.setAutoRepeatDelay(600)
        self.fixed_minus_button.setAutoRepeatInterval(10)
        self.fixed_minus_button.setObjectName("fixed_minus_button")
        self.verticalLayout_9.addWidget(self.fixed_minus_button)
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.amplitude_edit = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amplitude_edit.sizePolicy().hasHeightForWidth())
        self.amplitude_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.amplitude_edit.setFont(font)
        self.amplitude_edit.setObjectName("amplitude_edit")
        self.gridLayout.addWidget(self.amplitude_edit, 2, 0, 1, 1)
        self.frequency_edit = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frequency_edit.sizePolicy().hasHeightForWidth())
        self.frequency_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.frequency_edit.setFont(font)
        self.frequency_edit.setObjectName("frequency_edit")
        self.gridLayout.addWidget(self.frequency_edit, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.units_wildcard_0 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.units_wildcard_0.setFont(font)
        self.units_wildcard_0.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.units_wildcard_0.setObjectName("units_wildcard_0")
        self.horizontalLayout_4.addWidget(self.units_wildcard_0)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.apply_amplitude_button = QtWidgets.QPushButton(self.layoutWidget)
        self.apply_amplitude_button.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.apply_amplitude_button.setFont(font)
        self.apply_amplitude_button.setObjectName("apply_amplitude_button")
        self.gridLayout.addWidget(self.apply_amplitude_button, 2, 1, 1, 1)
        self.apply_frequency_button = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apply_frequency_button.sizePolicy().hasHeightForWidth())
        self.apply_frequency_button.setSizePolicy(sizePolicy)
        self.apply_frequency_button.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.apply_frequency_button.setFont(font)
        self.apply_frequency_button.setObjectName("apply_frequency_button")
        self.gridLayout.addWidget(self.apply_frequency_button, 4, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.frame_7 = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.measure_table = QtWidgets.QTableView(self.frame_7)
        self.measure_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.measure_table.setAlternatingRowColors(True)
        self.measure_table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.measure_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.measure_table.setTextElideMode(QtCore.Qt.ElideLeft)
        self.measure_table.setSortingEnabled(False)
        self.measure_table.setObjectName("measure_table")
        self.horizontalLayout.addWidget(self.measure_table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.save_point_button = QtWidgets.QPushButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_point_button.sizePolicy().hasHeightForWidth())
        self.save_point_button.setSizePolicy(sizePolicy)
        self.save_point_button.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.save_point_button.setFont(font)
        self.save_point_button.setObjectName("save_point_button")
        self.verticalLayout.addWidget(self.save_point_button)
        self.approach_point_button = QtWidgets.QPushButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.approach_point_button.sizePolicy().hasHeightForWidth())
        self.approach_point_button.setSizePolicy(sizePolicy)
        self.approach_point_button.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.approach_point_button.setFont(font)
        self.approach_point_button.setObjectName("approach_point_button")
        self.verticalLayout.addWidget(self.approach_point_button)
        self.delete_point_button = QtWidgets.QPushButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_point_button.sizePolicy().hasHeightForWidth())
        self.delete_point_button.setSizePolicy(sizePolicy)
        self.delete_point_button.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.delete_point_button.setFont(font)
        self.delete_point_button.setObjectName("delete_point_button")
        self.verticalLayout.addWidget(self.delete_point_button)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.start_stop_button = QtWidgets.QPushButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_stop_button.sizePolicy().hasHeightForWidth())
        self.start_stop_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.start_stop_button.setFont(font)
        self.start_stop_button.setObjectName("start_stop_button")
        self.verticalLayout.addWidget(self.start_stop_button)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.fixed_step_combobox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_7.setText(_translate("Form", "Статус подключения:"))
        self.usb_state_label.setText(_translate("Form", "Подключено"))
        self.label_4.setText(_translate("Form", "Статус калибратора:"))
        self.clb_state_label.setText(_translate("Form", "Остановлен"))
        self.groupBox.setTitle(_translate("Form", "Шаг"))
        self.label_2.setToolTip(_translate("Form", "Ctrl + колесо мыши"))
        self.label_2.setText(_translate("Form", "Грубый"))
        self.rough_plus_button.setText(_translate("Form", "+"))
        self.rough_minus_button.setText(_translate("Form", "-"))
        self.label_8.setToolTip(_translate("Form", "Колесо мыши"))
        self.label_8.setText(_translate("Form", "Обычный"))
        self.common_plus_button.setText(_translate("Form", "+"))
        self.common_minus_button.setText(_translate("Form", "-"))
        self.label_3.setToolTip(_translate("Form", "Shift + колесо мыши"))
        self.label_3.setText(_translate("Form", "Точный"))
        self.exact_plus_button.setText(_translate("Form", "+"))
        self.exact_minus_button.setText(_translate("Form", "-"))
        self.fixed_step_combobox.setToolTip(_translate("Form", "Ctrl + Shift + Колесо мыши"))
        self.fixed_step_combobox.setItemText(0, _translate("Form", "100 мкВ"))
        self.fixed_step_combobox.setItemText(1, _translate("Form", "10 мВ"))
        self.fixed_step_combobox.setItemText(2, _translate("Form", "100 мВ"))
        self.fixed_step_combobox.setItemText(3, _translate("Form", "1 В"))
        self.fixed_step_combobox.setItemText(4, _translate("Form", "10 В"))
        self.fixed_step_combobox.setItemText(5, _translate("Form", "20 В"))
        self.fixed_step_combobox.setItemText(6, _translate("Form", "100 В"))
        self.fixed_plus_button.setText(_translate("Form", "+"))
        self.fixed_minus_button.setText(_translate("Form", "-"))
        self.label_6.setText(_translate("Form", "Частота, Гц"))
        self.amplitude_edit.setText(_translate("Form", "0"))
        self.frequency_edit.setText(_translate("Form", "0"))
        self.label_5.setText(_translate("Form", "Амплитуда,"))
        self.units_wildcard_0.setText(_translate("Form", "В"))
        self.apply_amplitude_button.setText(_translate("Form", "✔"))
        self.apply_frequency_button.setText(_translate("Form", "✔"))
        self.save_point_button.setText(_translate("Form", "Сохранить\n"
"точку"))
        self.approach_point_button.setText(_translate("Form", "Перейти\n"
"к точке"))
        self.delete_point_button.setText(_translate("Form", "Удалить\n"
"точку"))
        self.start_stop_button.setText(_translate("Form", "Начать\n"
"поверку"))
