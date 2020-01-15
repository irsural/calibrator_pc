from PyQt5.QtWidgets import QLineEdit
import numpy as np


def parse_input(a_input: str):
    if not a_input:
        return 0.
    return float(a_input)


def update_edit_color(actual_value: float, a_edit: QLineEdit):
    try:
        amplitude = float(a_edit.text())
        if amplitude == actual_value:
            a_edit.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            a_edit.setStyleSheet("background-color: rgb(250, 250, 170);")
    except ValueError:
        a_edit.setStyleSheet("background-color: rgb(245, 206, 203);")


def deviation(a_lval: float, a_rval: float):
    if a_lval == 0 or a_rval == 0:
        return 0
    return (a_lval - a_rval) / a_lval * 100


def auto_calc_points(a_start: float, a_stop: float, a_step:float):
    if a_start == a_stop or a_step == 0:
        return []
    if a_stop < a_start:
        a_step *= -1

    points = np.arange(a_start, a_stop, a_step)
    points = np.append(a_stop, points)
    sorted_list = (-np.sort(-points)).tolist()
    rounded_list = [round(elem, 9) for elem in sorted_list]
    return rounded_list


def bound(a_value, a_min, a_max):
    return max(min(a_value, a_max), a_min)
