from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.template_list_form import Ui_Dialog as TemplateListForm
import utils


class TemplateListWindow(QtWidgets.QDialog):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = TemplateListForm()
        self.ui.setupUi(self)
        self.show()

        self.ui.accept_button.clicked.connect(self.choose_template)
        self.ui.template_list.itemDoubleClicked.connect(self.open_template)

        self.ui.cancel_button.clicked.connect(self.reject)

        self.ui.add_template_button.clicked.connect(self.create_new_template)
        self.ui.delete_template_button.clicked.connect(self.delete_template)
        self.ui.edit_template_button.clicked.connect(self.edit_template)

    @pyqtSlot()
    def choose_template(self):
        self.open_template(self.ui.template_list.currentItem())

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def open_template(self, a_item: QtWidgets.QListWidgetItem):
        print(a_item.text())

    @pyqtSlot()
    def create_new_template(self):
        QtWidgets.QListWidgetItem("item", self.ui.template_list)

    @pyqtSlot()
    def edit_template(self):
        print("edit")

    @pyqtSlot()
    def delete_template(self):
        self.ui.template_list.takeItem(self.ui.template_list.currentRow())
