from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QWidget

from custom_widgets.CustomLineEdit import QEditDoubleClick


class NonOverlappingPainter(QtWidgets.QStyledItemDelegate):
    """
    По каким то причинам это делает цвет выбранной ячейки прозрачным
    """
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        item_option = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(item_option, index)

        # if item_option.state & QStyle.State_Selected and not (item_option.state & QStyle.State_Active):
        #     item_option.palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, QtCore.Qt.red)

        QtWidgets.QApplication.style().drawControl(QStyle.CE_ItemViewItem, item_option, painter)


class TableEditDoubleClick(QtWidgets.QItemDelegate):
    def __init__(self, a_parent):
        super().__init__(a_parent)

    def createEditor(self, parent: QWidget, option, index: QtCore.QModelIndex) -> QWidget:
        return QEditDoubleClick(parent)


class NonOverlappingDoubleClick(NonOverlappingPainter, TableEditDoubleClick):
    def __init__(self, a_parent):
        super().__init__(a_parent)
