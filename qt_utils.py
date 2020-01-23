from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import QPoint
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import utils


QSTYLE_COLOR_WHITE = "background-color: rgb(255, 255, 255);"
QSTYLE_COLOR_YELLOW = "background-color: rgb(250, 250, 170);"
QSTYLE_COLOR_RED = "background-color: rgb(245, 206, 203);"


def update_edit_color(a_actual_value: float, a_current_value, a_edit: QLineEdit):
    try:
        if float(a_current_value) == a_actual_value:
            a_edit.setStyleSheet(QSTYLE_COLOR_WHITE)
        else:
            a_edit.setStyleSheet(QSTYLE_COLOR_YELLOW)
    except ValueError:
        a_edit.setStyleSheet(QSTYLE_COLOR_RED)


def get_wheel_steps(event: QWheelEvent):
    degrees_num = event.angleDelta() / 8
    steps_num: QPoint = degrees_num / 15
    return steps_num.y()


class QItemOnlyNumbers(QtWidgets.QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QtWidgets.QWidget, option, index: QtCore.QModelIndex):
        edit = QtWidgets.QLineEdit(parent)
        regex = QtCore.QRegExp("[0-9.]+")
        validator = QtGui.QRegExpValidator(regex, parent)
        edit.setValidator(validator)
        return edit


class QEditDoubleClick(QtWidgets.QLineEdit):
    """
    QLineEdit с добавлением выделения вещественных чисел по дабл клику
    """
    def __init__(self, a_parent=None):
        super().__init__(a_parent)
        self.select_span = None

    def mouseDoubleClickEvent(self, a_event: QtGui.QMouseEvent):
        super().mouseDoubleClickEvent(a_event)
        result = utils.find_number_re.finditer(self.text())
        if result:
            for num_match in result:
                begin, end = num_match.span()
                if begin <= self.cursorPosition() <= end:
                    self.setSelection(begin, end - begin)
                    break
        a_event.accept()
