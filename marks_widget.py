import sqlite3
from enum import IntEnum

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot


from ui.py.marks_widget import Ui_marks_widget as MarksWidgetForm
import calibrator_constants as clb
import qt_utils
import clb_dll


class MarksWidget(QtWidgets.QWidget):
    close_confirmed = pyqtSignal()

    class MarkColumns(IntEnum):
        NAME = 0
        TAG = 1
        VALUE = 2
        COUNT = 3

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
        self.cursor = self.connection.cursor()

        self.marks_table = a_db_table_name
        self.default_mode = a_default_mode

        self.items_changed = False

        value_column_name = "Значение\nпо умолчанию" if self.default_mode else "Значение"
        self.ui.marks_table.setHorizontalHeaderLabels(["Параметр", "Тэг", value_column_name])

        self.ui.add_mark_button.clicked.connect(self.add_new_row)
        self.ui.delete_mark_button.clicked.connect(self.delete_row)

        self.ui.marks_table.itemChanged.connect(self.mark_items_as_changed)

        self.fill_table_from_db()

        self.window_existing_timer = QtCore.QTimer()
        self.window_existing_timer.timeout.connect(self.window_existing_chech)
        self.window_existing_timer.start(3000)

    def window_existing_chech(self):
        print("Marks Widget")

    def fill_table_from_db(self):
        qt_utils.qtablewidget_clear(self.ui.marks_table)

        self.cursor.execute(f"select name, tag, default_value from {self.marks_table}")
        for row_data in self.cursor.fetchall():
            row = self.ui.marks_table.rowCount()
            self.ui.marks_table.insertRow(row)
            for column, text in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(text)
                if column in (self.MarkColumns.NAME, self.MarkColumns.TAG):
                    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                    item.setBackground(QtCore.Qt.lightGray)
                self.ui.marks_table.setItem(row, column, item)

        self.items_changed = False

    def add_new_row(self):
        row = self.ui.marks_table.rowCount()
        self.ui.marks_table.insertRow(row)

        for column in range(self.MarkColumns.COUNT):
            self.ui.marks_table.setItem(row, column, QtWidgets.QTableWidgetItem(""))

    def delete_row(self):
        if self.ui.marks_table.selectionModel().selectedRows():
            res = QtWidgets.QMessageBox.question(self, "Подтвердите действие", "Вы уверены, что хотите удалить "
                                                 "выбранные параметры?\nВыбранные параметры также будут удалены из "
                                                 "всех УЖЕ ПРОВЕДЕННЫХ измерений.", QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.Yes:
                qt_utils.qtablewidget_delete_selected(self.ui.marks_table)
                self.mark_items_as_changed()

    def mark_items_as_changed(self):
        self.items_changed = True

    def table_to_list(self):
        items = []
        for row in range(self.ui.marks_table.rowCount()):
            table_row = (self.ui.marks_table.item(row, self.MarkColumns.NAME).text(),
                         self.ui.marks_table.item(row, self.MarkColumns.TAG).text(),
                         self.ui.marks_table.item(row, self.MarkColumns.VALUE).text())

            if table_row[self.MarkColumns.NAME] and table_row[self.MarkColumns.TAG]:
                items.append(table_row)
            else:
                raise ValueError

        return items

    def save(self):
        if not self.items_changed:
            return True

        try:
            items = self.table_to_list()

            with self.connection:
                self.cursor.execute(f"delete from {self.marks_table}")

                self.cursor.executemany(f"insert into {self.marks_table} (name, tag, default_value) "
                                        f"values (?,?,?)", items)
            self.fill_table_from_db()

            return True
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Все поля 'Параметр' и 'Тэг' должны быть заполнены!",
                                           QtWidgets.QMessageBox.Ok)
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Имена параметров и тэги должны быть уникальны!",
                                           QtWidgets.QMessageBox.Ok)
            return False

