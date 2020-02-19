from typing import List

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets, QtGui, QtCore

from ui.py.edited_lsit_widget import Ui_Form as EditedListForm
from ui.py.ok_cancel_dialog import Ui_Dialog as OkCancelForm
from custom_widgets.CustomLineEdit import QEditDoubleClick
import utils


class EditedListWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, a_init_items=(), a_list_name="List name"):
        super().__init__(parent)

        self.ui = EditedListForm()
        self.ui.setupUi(self)
        self.ui.lsitname_label.setText(a_list_name)

        self.delete_key_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.ui.list_widget)
        self.delete_key_sc.activated.connect(self.delete_selected_row)

        self.ui.add_list_item_button.clicked.connect(self.add_list_item_button_clicked)
        self.ui.delete_list_item_button.clicked.connect(self.delete_selected_row)

        for item in a_init_items:
            self.add_item(item, False)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.ui.list_widget.hasFocus():
            key = event.key()
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                rows: List[QtWidgets.QListWidgetItem] = self.ui.list_widget.selectedItems()
                if rows:
                    self.ui.list_widget.editItem(rows[0])
        else:
            event.accept()

    def item_editing_finished(self, a_index: QtCore.QModelIndex):
        edit = self.ui.list_widget.itemFromIndex(a_index)
        edit.setText(self.process_input(edit.text()))

    def process_input(self, a_input):
        return a_input

    def add_item(self, a_init_value="0", a_edit_item=True):
        list_item = QtWidgets.QListWidgetItem(a_init_value, self.ui.list_widget)
        list_item.setFlags(int(list_item.flags()) | QtCore.Qt.ItemIsEditable)
        self.ui.list_widget.addItem(list_item)
        self.ui.list_widget.setCurrentItem(list_item)
        if a_edit_item:
            self.ui.list_widget.editItem(list_item)

    def delete_selected_row(self):
        self.ui.list_widget.takeItem(self.ui.list_widget.currentRow())

    def add_list_item_button_clicked(self):
        self.add_item()

    def __prepare_list(self):
        out_list = []
        for idx in range(self.ui.list_widget.count()):
            item = self.ui.list_widget.item(idx).text()
            if item not in out_list:
                out_list.append(item)
        return out_list

    @pyqtSlot()
    def get_list(self):
        return self.__prepare_list()


class QRegExpDelegator(QtWidgets.QItemDelegate):
    editing_finished = pyqtSignal(QtCore.QModelIndex)

    def __init__(self, parent, a_regexp_pattern):
        super().__init__(parent)
        self.regexp_pattern = a_regexp_pattern

    def createEditor(self, parent: QtWidgets.QWidget, option, index: QtCore.QModelIndex):
        edit = QEditDoubleClick(parent)
        regex = QtCore.QRegExp(self.regexp_pattern)
        validator = QtGui.QRegExpValidator(regex, parent)
        edit.setValidator(validator)
        return edit

    def destroyEditor(self, editor: QEditDoubleClick, index: QtCore.QModelIndex):
        self.editing_finished.emit(index)
        return super().destroyEditor(editor, index)


class EditedListOnlyNumbers(EditedListWidget):
    def __init__(self, parent=None, a_init_items=(), a_list_name="List name"):
        super().__init__(parent, a_init_items, a_list_name)

        delegator = QRegExpDelegator(self, utils.find_number_re.pattern)
        delegator.editing_finished.connect(self.item_editing_finished)
        self.ui.list_widget.setItemDelegate(delegator)

    def process_input(self, a_input: str):
        value = float(a_input.replace(",", "."))
        return utils.float_to_string(value)


class EditedListWithUnits(EditedListWidget):
    def __init__(self, parent=None, units: str = "В", a_init_items=(), a_list_name="List name"):
        super().__init__(parent, a_init_items, a_list_name)

        delegator = QRegExpDelegator(self, utils.check_input_no_python_re.pattern)
        delegator.editing_finished.connect(self.item_editing_finished)
        self.ui.list_widget.setItemDelegate(delegator)

        self.units = units

    def process_input(self, a_input: str):
        try:
            processed_value = utils.parse_input(a_input)
        except ValueError:
            processed_value = 0
        return utils.value_to_user_with_units(self.units)(processed_value)

    def prepare_list(self) -> List[float]:
        out_list = []
        try:
            for idx in range(self.ui.list_widget.count()):
                item = self.ui.list_widget.item(idx).text()
                if item not in out_list:
                    out_list.append(utils.parse_input(item))
            return out_list
        except ValueError:
            return list()


class OkCancelDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, a_title="Dialog"):
        super().__init__(parent)

        self.ui = OkCancelForm()
        self.ui.setupUi(self)
        self.setWindowTitle(a_title)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)
