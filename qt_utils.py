from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import QPoint


def update_edit_color(a_actual_value: float, a_current_value, a_edit: QLineEdit):
    try:
        if float(a_current_value) == a_actual_value:
            a_edit.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            a_edit.setStyleSheet("background-color: rgb(250, 250, 170);")
    except ValueError:
        a_edit.setStyleSheet("background-color: rgb(245, 206, 203);")


def get_wheel_steps(event: QWheelEvent):
    degrees_num = event.angleDelta() / 8
    steps_num: QPoint = degrees_num / 15
    return steps_num.y()
