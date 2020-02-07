from math import isclose

from PyQt5 import QtCore, QtWidgets, QtGui

import constants


QSTYLE_COLOR_WHITE = "background-color: rgb(255, 255, 255);"
QSTYLE_COLOR_YELLOW = "background-color: rgb(250, 250, 170);"
QSTYLE_COLOR_RED = "background-color: rgb(245, 206, 203);"


def update_edit_color(a_actual_value, a_current_value, a_edit: QtWidgets.QLineEdit):
    try:
        if isclose(a_actual_value, float(a_current_value), rel_tol=constants.FLOAT_EPSILON):
            a_edit.setStyleSheet(QSTYLE_COLOR_WHITE)
        else:
            a_edit.setStyleSheet(QSTYLE_COLOR_YELLOW)
    except ValueError:
        a_edit.setStyleSheet(QSTYLE_COLOR_RED)


def get_wheel_steps(event: QtGui.QWheelEvent):
    degrees_num = event.angleDelta() / 8
    steps_num: QtCore.QPoint = degrees_num / 15
    return steps_num.y()


def qtablewidget_append_row(a_table: QtWidgets.QTableWidget, a_row_data: tuple):
    row_num = a_table.rowCount()
    a_table.insertRow(row_num)
    for col, data in enumerate(a_row_data):
        a_table.setItem(row_num, col, QtWidgets.QTableWidgetItem(str(data)))

def qtablewidget_clear(a_table: QtWidgets.QTableWidget):
    """
    В отличии от QTableWidget.clear не удаляет заголовки таблицы и
    В отличии от QTableWidget.clearContents удаляет строки, вместо простого их очищения
    :param a_table: QTableWidget
    :return:
    """
    for row in range(a_table.rowCount()):
        a_table.removeRow(row)
