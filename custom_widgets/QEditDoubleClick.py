from PyQt5 import QtWidgets, QtGui

import utils


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

