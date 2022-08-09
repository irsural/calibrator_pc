from enum import IntEnum
import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal


from ui.py.marks_widget import Ui_marks_widget as MarksWidgetForm
from irspy.qt.qt_settings_ini_parser import QtSettings
from irspy.qt import qt_utils
from irspy import utils


class MarksWidget(QtWidgets.QWidget):
    close_confirmed = pyqtSignal()

    class MarkColumns(IntEnum):
        NAME = 0
        TAG = 1
        VALUE = 2
        COUNT = 3

    def __init__(self, a_caller_name: str, a_settings: QtSettings, a_db_connection: sqlite3.Connection, a_measure_id=None,
                 a_parent=None):
        """
        Виджет, который управляет дополнительными параметрами измерений
        :param a_caller_name: Имя вызывающего класса, нужно для сохранение настроек
        :param a_db_connection: Соединение с базой данных
        :param a_measure_id: Если не задано, то виджет используется в режиме default_mode
                            В режиме default_mode последняя колонка таблицы является значением по умолчанию, в
                            противном случае, последняя колонка является значением параметра для конкретного измерения
                            и при изменении этой колонки в a_db_table_name:value всегда записывается пустая строка
        :param a_parent: родитель виджета
        """
        super().__init__(a_parent)

        self.ui = MarksWidgetForm()
        self.ui.setupUi(self)

        self.ui.add_mark_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/icons/plus.png")))
        self.ui.delete_mark_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/icons/minus2.png")))

        self.parent = a_parent
        self.settings_geometry_name = '.'.join([a_caller_name, self.__class__.__name__])

        self.settings = a_settings

        self.ui.marks_table.horizontalHeader().restoreState(
            self.settings.read_bytes(self.settings_geometry_name))

        self.connection = a_db_connection
        self.cursor = self.connection.cursor()

        self.default_mode = True if a_measure_id is None else False
        self.measure_id = a_measure_id

        self.items_changed = False
        self.deleted_names = []

        value_column_name = "Значение\nпо умолчанию" if self.default_mode else "Значение"
        self.ui.marks_table.setHorizontalHeaderLabels(["Параметр", "Тэг", value_column_name])

        self.ui.add_mark_button.clicked.connect(self.add_new_row)
        self.ui.delete_mark_button.clicked.connect(self.delete_row)

        self.ui.marks_table.itemChanged.connect(self.mark_items_as_changed)
        self.ui.marks_table.customContextMenuRequested.connect(self.chow_table_custom_menu)

        self.fill_table_from_db()

    @staticmethod
    def qtablewidget_clear(a_table: QtWidgets.QTableWidget):
        for row in reversed(range(a_table.rowCount())):
            a_table.removeRow(row)

    def fill_table_from_db(self):
        self.qtablewidget_clear(self.ui.marks_table)

        if self.default_mode:
            self.cursor.execute("select name, tag, default_value from marks")
        else:
            # Вероятно, это дерьмовый запрос и его можно написать лучше
            self.cursor.execute("select m.name, m.tag, v.value from marks m "
                                "left outer join "
                                "(select mark_name, value, measure_id from mark_values v where v.measure_id = "
                                "{0}) v on m.name = v.mark_name".format(self.measure_id))

        for row_data in self.cursor.fetchall():
            row = self.ui.marks_table.rowCount()
            self.ui.marks_table.insertRow(row)
            for column, text in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(text)
                if column in (self.MarkColumns.NAME, self.MarkColumns.TAG):
                    # noinspection PyTypeChecker
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

    @utils.exception_decorator_print
    def delete_row(self, _):
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

    def mark_items_as_changed(self):
        self.items_changed = True

    def is_row_in_db(self, a_row: int) -> bool:
        item_flags = self.ui.marks_table.item(a_row, self.MarkColumns.NAME).flags()
        return not (item_flags & QtCore.Qt.ItemIsEditable)

    def get_marks_map(self):
        """
        :return: Список кортежей (тэг, значение)
        """
        return [(self.ui.marks_table.item(row, MarksWidget.MarkColumns.TAG).text(),
                 self.ui.marks_table.item(row, MarksWidget.MarkColumns.VALUE).text())
                for row in range(self.ui.marks_table.rowCount())]

    def get_names_map(self):
        """
        :return: Список кортежей (имя, значение)
        """
        return [(self.ui.marks_table.item(row, MarksWidget.MarkColumns.NAME).text(),
                 self.ui.marks_table.item(row, MarksWidget.MarkColumns.VALUE).text())
                for row in range(self.ui.marks_table.rowCount())]

    def __table_to_list(self):
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
                items = self.__table_to_list()
                with self.connection:
                    self.cursor.executemany("delete from marks where name = ?", self.deleted_names)
                    self.cursor.executemany("delete from mark_values where mark_name = ?", self.deleted_names)
                    for row, data in items:
                        row_exist = self.is_row_in_db(row)
                        if self.default_mode:
                            if row_exist:
                                # Значания по умолчанию обновляем только в режиме "по умолчанию"
                                self.cursor.execute("update marks set default_value = ? where name = ?",
                                                    (data[self.MarkColumns.VALUE], data[self.MarkColumns.NAME]))
                            else:
                                self.cursor.execute("insert into marks (name, tag, default_value) "
                                                    "values (?,?,?)", data)
                        else:
                            if not row_exist:
                                # В режиме не "по умолчанию" значания по умолчанию оставляем пустыми
                                self.cursor.execute("insert into marks (name, tag, default_value) "
                                                    "values (?,?,?)",
                                                    (data[self.MarkColumns.NAME], data[self.MarkColumns.TAG], ""))
                            if data[self.MarkColumns.VALUE]:
                                # Если значение не пусто, добавляем его в таблицу значений
                                self.cursor.execute("select * from mark_values where mark_name = ? and measure_id = ?",
                                                    (data[self.MarkColumns.NAME], self.measure_id))
                                if not self.cursor.fetchone():
                                    self.cursor.execute("insert into mark_values "
                                                        "(value, mark_name, measure_id) values(?,?,?) ",
                                                        (data[self.MarkColumns.VALUE], data[self.MarkColumns.NAME],
                                                         self.measure_id))
                                else:
                                    self.cursor.execute("update mark_values set value = ? "
                                                        "where mark_name = ? and measure_id = ?",
                                                        (data[self.MarkColumns.VALUE], data[self.MarkColumns.NAME],
                                                         self.measure_id))

                            else:
                                self.cursor.execute("delete from mark_values "
                                                    "where mark_name = ? and measure_id = ?",
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

    def chow_table_custom_menu(self, a_position: QtCore.QPoint):
        menu = QtWidgets.QMenu(self)
        copy_cell_act = menu.addAction("Копировать")
        copy_cell_act.triggered.connect(self.copy_cell_text_to_clipboard)
        menu.popup(self.ui.marks_table.viewport().mapToGlobal(a_position))

    def copy_cell_text_to_clipboard(self):
        text = self.ui.marks_table.currentItem().text()
        QtWidgets.QApplication.clipboard().setText(text)

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_bytes(
            self.settings_geometry_name, self.ui.marks_table.horizontalHeader().saveState())
