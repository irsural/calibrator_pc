from ui.py.edited_lsit_form import Ui_Dialog as EditedListForm
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import qt_utils


class EditedListDialog(QDialog):
    results_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.ui = EditedListForm()
        self.ui.setupUi(self)
        self.ui.lsitname_label.setText("Частота, Гц")
        self.setWindowTitle("Редактирование частот поверки")

        self.delete_key_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.ui.list_widget)
        self.delete_key_sc.activated.connect(lambda: self.ui.list_widget.takeItem(self.ui.list_widget.currentRow()))

        self.ui.list_widget.setItemDelegate(qt_utils.QItemOnlyNumbers(self))

        self.ui.add_list_item_button.clicked.connect(self.add_frequency)

    def add_frequency(self):
        list_item = QtWidgets.QListWidgetItem("0", self.ui.list_widget)
        list_item.setFlags(int(list_item.flags()) | QtCore.Qt.ItemIsEditable)
        self.ui.list_widget.addItem(list_item)
        self.ui.list_widget.editItem(list_item)

    def list_to_string(self):
        frequency_list = []
        for idx in range(self.ui.list_widget.count()):
            frequency = self.ui.list_widget.item(idx).text()
            if frequency not in frequency_list:
                frequency_list += frequency

        return ";".join(frequency_list)

    @pyqtSlot()
    def accept(self):
        self.results_ready.emit(self.list_to_string())
        self.done(QDialog.Accepted)

