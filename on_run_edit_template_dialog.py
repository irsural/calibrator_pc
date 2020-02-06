from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.on_run_edit_template_form import Ui_Dialog as OnRunEditTemplateForm
import utils


class OnRunEditTemplateDialog(QtWidgets.QDialog):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = OnRunEditTemplateForm()
        self.ui.setupUi(self)
        self.show()
