import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot


from ui.py.marks_widget import Ui_marks_widget as MarksWidgetForm
import calibrator_constants as clb
import clb_dll


class MarksWidget(QtWidgets.QWidget):
    close_confirmed = pyqtSignal()

    def __init__(self, a_db_connection: sqlite3.Connection, a_db_table_name: str, a_default_mode: bool, a_parent=None):
        """
        Виджет, который управляет дополнительными параметрами измерений
        :param a_db_connection: Соединение с базой данных, в которой содержится таблица a_db_table_name
        :param a_db_table_name: Название таблицы, в которой содержатся имена и тэги
        :param a_default_mode: В режиме a_default_mode последняя колонка таблицы является значением по умолчанию, в
                            противном случае, последняя колонка является значением параметра для конкретного измерения
        :param a_parent: родитель виджета
        """
        super().__init__(a_parent)

        self.ui = MarksWidgetForm()
        self.ui.setupUi(self)

        self.connection = a_db_connection
        self.marks_table = a_db_table_name
        self.default_mode = a_default_mode

        value_column_name = "Значение\nпо умолчанию" if self.default_mode else "Значение"
        self.ui.marks_table.setHorizontalHeaderLabels(["Параметр", "Тэг", value_column_name])

        self.ui.add_mark_button.clicked.connect(self.add_mark)
        self.ui.delete_mark_button.clicked.connect(self.delete_mark)

        self.ui.marks_table.itemChanged.connect(self.show_confirm_changes_dialog)

        self.window_existing_timer = QtCore.QTimer()
        self.window_existing_timer.timeout.connect(self.window_existing_chech)
        self.window_existing_timer.start(3000)

    def window_existing_chech(self):
        print("Marks Widget")

    def add_mark(self):
        pass

    def delete_mark(self):
        pass

    def show_confirm_changes_dialog(self):
        pass

    def save(self):
        pass
