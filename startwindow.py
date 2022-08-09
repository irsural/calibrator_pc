from sqlite3 import Connection

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore, QtSql

from ui.py.startform import Ui_start_dialog as StartForm
from db_measures import MeasureColumn, MEASURE_COLUMN_TO_NAME, MeasuresDB
from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from create_protocol_dialog import CreateProtocolDialog
from irspy.qt.qt_settings_ini_parser import QtSettings
from irspy.qt import qt_utils
from irspy import utils


class StartWindow(QtWidgets.QWidget):
    source_mode_chosen = pyqtSignal()
    no_template_mode_chosen = pyqtSignal()
    template_mode_chosen = pyqtSignal()

    def __init__(self, a_control_db_connection: Connection, a_db_name: str, a_settings: QtSettings,
                 a_parent: QtWidgets.QMainWindow = None):
        """
        Для отображения таблицы измерений используется QSqlRelationalTableModel (это сильно упрощает жизнь)
        При этом для остальных операций (добавление, удаление) используется другое соединение sqlite3.Connection
        Соединения могут быть подключены к БД параллельно
        :param a_control_db_connection: Соединения для управления БД
        :param a_db_name: Имя файла БД
        :param a_settings: Настройки в ini
        :param a_parent: Widget parent
        """
        super().__init__(a_parent)

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.settings = a_settings

        self.setWindowTitle("Калибратор N4-25")

        self.ui.source_mode_button.clicked.connect(self.source_mode_chosen)
        self.ui.no_template_mode_button.clicked.connect(self.no_template_mode_chosen)
        self.ui.template_mode_button.clicked.connect(self.template_mode_chosen)

        self.ui.create_protocol_button.clicked.connect(self.create_protocol)
        self.ui.measures_table.doubleClicked.connect(self.create_protocol)

        self.parent.show()
        self.parent.setObjectName("start_window")
        self.settings.restore_qwidget_state(self.parent)

        self.control_db_connection = a_control_db_connection
        self.measure_db = MeasuresDB(a_control_db_connection)

        self.display_db_connection = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.display_db_model = QtSql.QSqlRelationalTableModel(self)
        self.sort_proxy_model = CustomSortingModel(self)
        self.header_context = self.config_measure_table(a_db_name)

    def config_measure_table(self, a_db_name: str):
        self.display_db_connection.setDatabaseName(a_db_name)
        res = self.display_db_connection.open()
        assert res, "Can't open database {0}!".format(a_db_name)

        self.display_db_model.setTable("measures")
        self.display_db_model.setRelation(MeasureColumn.DEVICE_SYSTEM,
                                          QtSql.QSqlRelation("system", "id", "name"))

        for column in range(self.display_db_model.columnCount()):
            self.display_db_model.setHeaderData(column, QtCore.Qt.Horizontal, MEASURE_COLUMN_TO_NAME[column])

        self.sort_proxy_model.setSourceModel(self.display_db_model)
        self.ui.measures_table.setModel(self.sort_proxy_model)

        # Чтобы был приятный цвет выделения
        self.ui.measures_table.setItemDelegate(NonOverlappingDoubleClick(self.ui.measures_table))

        self.ui.measures_table.selectionModel().currentChanged.connect(self.current_selection_changed)
        self.ui.measures_table.selectionModel().modelChanged.connect(self.current_selection_changed)
        self.ui.measures_table.selectionModel().selectionChanged.connect(self.current_selection_changed)

        self.settings.restore_qwidget_state(self.ui.measures_table)
        self.ui.measures_table.setColumnHidden(MeasureColumn.ID, True)

        header_context = qt_utils.TableHeaderContextMenu(self, self.ui.measures_table, True)
        self.ui.measures_table.horizontalHeader().setSectionsMovable(True)
        self.ui.measures_table.customContextMenuRequested.connect(self.show_table_custom_menu)

        self.update_table()
        return header_context

    def current_selection_changed(self):
        measure_id = self.get_selected_id()
        if measure_id is None:
            self.ui.create_protocol_button.setEnabled(False)
        else:
            self.ui.create_protocol_button.setEnabled(True)

    def update_table(self):
        self.display_db_model.select()
        self.current_selection_changed()

    @utils.exception_decorator_print
    def create_protocol(self, _):
        measure_id = self.get_selected_id()
        assert measure_id is not None, "measure id must not be None!"
        create_protocol_dialog = CreateProtocolDialog(
            self.settings, measure_id, self.control_db_connection, self)
        create_protocol_dialog.exec()
        self.update_table()

    def show_table_custom_menu(self, a_position: QtCore.QPoint):
        menu = QtWidgets.QMenu(self)
        delete_measure_act = menu.addAction("Удалить измерение")
        delete_measure_act.triggered.connect(self.delete_measure)
        menu.popup(self.ui.measures_table.viewport().mapToGlobal(a_position))

    def delete_measure(self):
        measure_id = self.get_selected_id()
        if measure_id is not None:
            reply = QtWidgets.QMessageBox.question(self, "Подтвердите действие", "Вы действительно хотите удалить "
                                                   "выбранное измерение?", QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.measure_db.delete(measure_id)
                self.update_table()

    def get_selected_id(self):
        selected = self.ui.measures_table.selectionModel().selectedRows()
        if selected:
            selected_row = selected[0].row()
            measure_id = self.sort_proxy_model.index(selected_row, MeasureColumn.ID).data()
            return measure_id
        else:
            return None

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_qwidget_state(self.parent)
        self.settings.save_qwidget_state(self.ui.measures_table)
        self.display_db_connection.close()
        self.header_context.delete_connections()
        a_event.accept()


class CustomSortingModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left, right):
        if left.column() == MeasureColumn.DATETIME:
            date_left = QtCore.QDateTime.fromString(left.data(), "dd.MM.yyyy H:mm:ss")
            date_right = QtCore.QDateTime.fromString(right.data(), "dd.MM.yyyy H:mm:ss")

            return date_left < date_right
        else:
            return super().lessThan(left, right)
