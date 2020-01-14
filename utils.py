from PyQt5.QtWidgets import QLineEdit

def parse_input(a_input: str):
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
