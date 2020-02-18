import sqlite3
from enum import IntEnum

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal


from ui.py.marks_widget import Ui_marks_widget as MarksWidgetForm
from db_measures import MeasureTables
import qt_utils
import utils


class Mark:
    # Сделать namedtuple?
    def __init__(self, a_name="", a_tag="", a_value=""):
        self.name = a_name
        self.tag = a_tag
        self.value = a_value


class MarksWidget(QtWidgets.QWidget):
    close_confirmed = pyqtSignal()

    class MarkColumns(IntEnum):
        NAME = 0
        TAG = 1
        VALUE = 2
        COUNT = 3

    def __init__(self, a_db_connection: sqlite3.Connection, a_db_tables: MeasureTables, a_measure_id=None,
                 a_parent=None):
        """
        Виджет, который управляет дополнительными параметрами измерений
        :param a_db_connection: Соединение с базой данных, в которой содержится таблица a_db_table_name
        :param a_db_table_name: Название таблицы, в которой содержатся имена и тэги
        :param a_measure_id: Если не задано, то виджет используется в режиме default_mode
                            В режиме default_mode последняя колонка таблицы является значением по умолчанию, в
                            противном случае, последняя колонка является значением параметра для конкретного измерения
                            и при изменении этой колонки в a_db_table_name:value всегда записывается пустая строка
        :param a_parent: родитель виджета
        """
        super().__init__(a_parent)

        self.ui = MarksWidgetForm()
        self.ui.setupUi(self)

        self.connection = a_db_connection
        self.cursor = self.connection.cursor()

        self.marks_table = a_db_tables.marks_table
        self.mark_values_table = a_db_tables.mark_values_table
        self.default_mode = True if a_measure_id is None else False
        self.measure_id = a_measure_id

        self.items_changed = False
        self.deleted_names = []

        value_column_name = "Значение\nпо умолчанию" if self.default_mode else "Значение"
        self.ui.marks_table.setHorizontalHeaderLabels(["Параметр", "Тэг", value_column_name])

        self.ui.add_mark_button.clicked.connect(self.add_new_row)
        self.ui.delete_mark_button.clicked.connect(self.delete_row)

        self.ui.marks_table.itemChanged.connect(self.mark_items_as_changed)

        self.fill_table_from_db()

    def fill_table_from_db(self):
        qt_utils.qtablewidget_clear(self.ui.marks_table)
        if self.default_mode:
            self.cursor.execute(f"select name, tag, default_value from {self.marks_table}")
        else:
            # Вероятно, это дерьмовый запрос
            self.cursor.execute(f"select m.name, m.tag, v.value from marks m "
                                f"left outer join "
                                f"(select mark_name, value, measure_id from mark_values v where v.measure_id = "
                                f"{self.measure_id}) v on m.name = v.mark_name")

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
        self.deleted_names.clear()

    def add_new_row(self):
        row = self.ui.marks_table.rowCount()
        self.ui.marks_table.insertRow(row)

        for column in range(self.MarkColumns.COUNT):
            self.ui.marks_table.setItem(row, column, QtWidgets.QTableWidgetItem(""))

    def delete_row(self):
        try:
            rows = self.ui.marks_table.selectionModel().selectedRows()
            if rows:
                res = QtWidgets.QMessageBox.question(self, "Подтвердите действие", "Вы уверены, что хотите удалить "
                                                     "выбранные параметры?\nВыбранные параметры также будут удалены из "
                                                     "всех УЖЕ ПРОВЕДЕННЫХ измерений.", QtWidgets.QMessageBox.Yes |
                                                     QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if res == QtWidgets.QMessageBox.Yes:
                    for idx_model in reversed(rows):
                        row = idx_model.row()
                        if self.is_row_in_db(row):
                            self.deleted_names.append((self.ui.marks_table.item(row, self.MarkColumns.NAME).text(),))
                        self.ui.marks_table.removeRow(row)
                    self.items_changed = True
        except Exception as err:
            utils.exception_handler(err)

    def mark_items_as_changed(self, a_item: QtWidgets.QTableWidgetItem):
        self.items_changed = True
        # if self.default_mode:
        # elif a_item.column() != self.MarkColumns.VALUE:
        #     self.items_changed = True

    def is_row_in_db(self, a_row: int) -> bool:
        item_flags = self.ui.marks_table.item(a_row, self.MarkColumns.NAME).flags()
        return not (item_flags & QtCore.Qt.ItemIsEditable)

    def table_to_list(self):
        items = []
        for row in range(self.ui.marks_table.rowCount()):
            row_data = (self.ui.marks_table.item(row, self.MarkColumns.NAME).text(),
                        self.ui.marks_table.item(row, self.MarkColumns.TAG).text(),
                        self.ui.marks_table.item(row, self.MarkColumns.VALUE).text())

            if row_data[self.MarkColumns.NAME] and row_data[self.MarkColumns.TAG]:
                items.append((row, row_data))
            else:
                raise ValueError

        return items

    def save(self):
        try:
            if self.items_changed:
                items = self.table_to_list()
                with self.connection:
                    self.cursor.executemany(f"delete from {self.marks_table} where name = ?", self.deleted_names)
                    self.cursor.executemany(f"delete from {self.mark_values_table} where mark_name = ?",
                                            self.deleted_names)
                    for row, data in items:
                        row_exist = self.is_row_in_db(row)
                        if self.default_mode:
                            if row_exist:
                                # Значания по умолчанию обновляем только в режиме "по умолчанию"
                                self.cursor.execute(f"update {self.marks_table} set default_value = ? where name = ?",
                                                    (data[self.MarkColumns.VALUE], data[self.MarkColumns.NAME]))
                            else:
                                self.cursor.execute(f"insert into {self.marks_table} (name, tag, default_value) "
                                                    f"values (?,?,?)", data)
                        else:
                            if not row_exist:
                                # В режиме не "по умолчанию" значания по умолчанию оставляем пустыми
                                self.cursor.execute(f"insert into {self.marks_table} (name, tag, default_value) "
                                                    f"values (?,?,?)",
                                                    (data[self.MarkColumns.NAME], data[self.MarkColumns.TAG], ""))
                            print(data)
                            if data[self.MarkColumns.VALUE]:
                                # Если значение не пусто, добавляем его в таблицу значений
                                self.cursor.execute(f"insert into {self.mark_values_table} "
                                                    f"(value, mark_name, measure_id) values(?,?,?)"
                                                    f"on conflict (mark_name, measure_id) do update set value = ?",
                                                    (data[self.MarkColumns.VALUE],
                                                     data[self.MarkColumns.NAME],
                                                     self.measure_id,
                                                     data[self.MarkColumns.VALUE]))
                            else:
                                print("delete")
                                self.cursor.execute(f"delete from {self.mark_values_table} "
                                                    f"where mark_name = ? and measure_id = ?",
                                                    (data[self.MarkColumns.NAME], self.measure_id))

                self.fill_table_from_db()

            return True
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Все поля 'Параметр' и 'Тэг' должны быть заполнены!",
                                           QtWidgets.QMessageBox.Ok)
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Имена параметров и тэги должны быть уникальны!",
                                           QtWidgets.QMessageBox.Ok)
            return False
