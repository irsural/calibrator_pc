from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets, QtGui, QtCore

from ui.py.edited_lsit_form import Ui_Dialog as EditedListForm
from custom_widgets.QEditDoubleClick import QEditDoubleClick
import utils


class EditedListDialog(QDialog):
    list_ready = pyqtSignal(list)

    def __init__(self, parent=None, a_init_items=(), a_title="Title", a_list_name="List name"):
        super().__init__(parent)

        self.ui = EditedListForm()
        self.ui.setupUi(self)
        self.setWindowTitle(a_title)
        self.ui.lsitname_label.setText(a_list_name)
        self.show()

        self.delete_key_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.ui.list_widget)
        self.delete_key_sc.activated.connect(self.delete_selected_row)

        self.ui.add_list_item_button.clicked.connect(self.add_list_item_button_clicked)
        self.ui.delete_list_item_button.clicked.connect(self.delete_selected_row)

        for item in a_init_items:
            self.add_item(item, False)

    def add_item(self, a_init_value="0", a_edit_item=True):
        list_item = QtWidgets.QListWidgetItem(a_init_value, self.ui.list_widget)
        list_item.setFlags(int(list_item.flags()) | QtCore.Qt.ItemIsEditable)
        self.ui.list_widget.addItem(list_item)
        if a_edit_item:
            self.ui.list_widget.editItem(list_item)

    def delete_selected_row(self):
        self.ui.list_widget.takeItem(self.ui.list_widget.currentRow())

    def add_list_item_button_clicked(self):
        self.add_item()

    def prepare_list(self):
        out_list = []
        for idx in range(self.ui.list_widget.count()):
            item = self.ui.list_widget.item(idx).text()
            if item not in out_list:
                out_list.append(item)
        return out_list

    @pyqtSlot()
    def accept(self):
        self.list_ready.emit(self.prepare_list())
        self.done(QDialog.Accepted)


class QItemOnlyNumbers(QtWidgets.QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QtWidgets.QWidget, option, index: QtCore.QModelIndex):
        edit = QEditDoubleClick(parent)
        regex = QtCore.QRegExp(utils.find_number_re.pattern)
        validator = QtGui.QRegExpValidator(regex, parent)
        edit.setValidator(validator)
        return edit


class EditedListOnlyNumbers(EditedListDialog):
    def __init__(self, parent=None, a_init_items=(), a_title="Title", a_list_name="List name"):
        super().__init__(parent, a_init_items, a_title, a_list_name)
        self.ui.list_widget.setItemDelegate(QItemOnlyNumbers(self))


class EditedListWithUnits(EditedListDialog):
    def __init__(self, parent=None, a_init_items=(), a_title="Title", a_list_name="List name"):
        super().__init__(parent, a_init_items, a_title, a_list_name)
        self.ui.list_widget.setItemDelegate(QItemOnlyNumbers(self))
