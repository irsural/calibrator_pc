from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.edit_template_form import Ui_Dialog as EditTemplateForm
import utils


class EditTemplateDialog(QtWidgets.QDialog):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = EditTemplateForm()
        self.ui.setupUi(self)
        self.show()
