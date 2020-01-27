from PyQt5 import QtCore, QtWidgets, QtGui


QSTYLE_COLOR_WHITE = "background-color: rgb(255, 255, 255);"
QSTYLE_COLOR_YELLOW = "background-color: rgb(250, 250, 170);"
QSTYLE_COLOR_RED = "background-color: rgb(245, 206, 203);"


def update_edit_color(a_actual_value: float, a_current_value, a_edit: QtWidgets.QLineEdit):
    try:
        if float(a_current_value) == a_actual_value:
            a_edit.setStyleSheet(QSTYLE_COLOR_WHITE)
        else:
            a_edit.setStyleSheet(QSTYLE_COLOR_YELLOW)
    except ValueError:
        a_edit.setStyleSheet(QSTYLE_COLOR_RED)


def get_wheel_steps(event: QtGui.QWheelEvent):
    degrees_num = event.angleDelta() / 8
    steps_num: QtCore.QPoint = degrees_num / 15
    return steps_num.y()
