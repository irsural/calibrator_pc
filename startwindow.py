from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore

from ui.py.startform import Ui_Form as StartForm


class StartWindow(QtWidgets.QWidget):
    source_mode_chosen = pyqtSignal()
    no_template_mode_chosen = pyqtSignal()
    template_mode_chosen = pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.show()

        self.ui.source_mode_button.clicked.connect(self.source_mode_chosen)
        self.ui.no_template_mode_button.clicked.connect(self.no_template_mode_chosen)
        self.ui.template_mode_button.clicked.connect(self.template_mode_chosen)

        self.window_existing_timer = QtCore.QTimer()
        self.window_existing_timer.timeout.connect(self.window_existing_chech)
        self.window_existing_timer.start(3000)

    def window_existing_chech(self):
        print("Start Window")

