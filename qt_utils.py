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
