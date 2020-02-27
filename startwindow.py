from sqlite3 import Connection

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore, QtSql

from ui.py.startform import Ui_Form as StartForm
from db_measures import MeasureTables, MeasureColumn, MEASURE_COLUMN_TO_NAME, MeasuresDB
from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from settings_ini_parser import Settings
import qt_utils
import utils

class StartWindow(QtWidgets.QWidget):
    source_mode_chosen = pyqtSignal()
    no_template_mode_chosen = pyqtSignal()
    template_mode_chosen = pyqtSignal()

    def __init__(self, a_control_db_connection: Connection, a_db_name: str, a_db_tables: MeasureTables,
                 a_settings: Settings, a_parent=None):
        """
        Для отображения таблицы измерений используется QSqlRelationalTableModel (это сильно упрощает жизнь)
        При этом для остальных операций (добавление, удаление) используется другое соединение sqlite3.Connection
        Соединения могут быть подключены к БД параллельно
        :param a_control_db_connection: Соединения для управления БД
        :param a_db_name: Имя файла БД
        :param a_db_tables: Названия таблиц БД
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

        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.parent.show()
        # По каким то причинам restoreGeometry не восстанавливает размер MainWindow, если оно скрыто
        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        self.display_db_connection = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.display_db_model = QtSql.QSqlRelationalTableModel(self)
        self.sort_proxy_model = QtCore.QSortFilterProxyModel(self)
        self.header_context = self.config_measure_table(a_db_name, a_db_tables)

        self.control_db_connection = MeasuresDB(a_control_db_connection, a_db_tables)

    def config_measure_table(self, a_db_name: str, a_tables: MeasureTables):
        self.display_db_connection.setDatabaseName(a_db_name)
        res = self.display_db_connection.open()
        assert res, f"Can't open database {a_db_name}!"

        self.display_db_model.setTable(a_tables.measures_table)
        self.display_db_model.setRelation(MeasureColumn.DEVICE_SYSTEM,
                                          QtSql.QSqlRelation(a_tables.system_table, "id", "name"))
        self.display_db_model.setRelation(MeasureColumn.SIGNAL_TYPE,
                                          QtSql.QSqlRelation(a_tables.signal_type_table, "id", "name"))

        for column in range(self.display_db_model.columnCount()):
            self.display_db_model.setHeaderData(column, QtCore.Qt.Horizontal, MEASURE_COLUMN_TO_NAME[column])

        self.sort_proxy_model.setSourceModel(self.display_db_model)
        self.ui.measures_table.setModel(self.sort_proxy_model)

        # Чтобы был приятный цвет выделения
        self.ui.measures_table.setItemDelegate(NonOverlappingDoubleClick(self))

        self.ui.measures_table.selectionModel().currentChanged.connect(self.activate_create_protocol_button)

        self.ui.measures_table.horizontalHeader().restoreState(self.settings.get_last_header_state(
            self.__class__.__name__))
        self.ui.measures_table.setColumnHidden(MeasureColumn.ID, True)

        header_context = qt_utils.TableHeaderContextMenu(self, self.ui.measures_table, True)
        self.ui.measures_table.horizontalHeader().setSectionsMovable(True)
        self.ui.measures_table.customContextMenuRequested.connect(self.chow_table_custom_menu)

        self.display_db_model.select()

        return header_context

    def activate_create_protocol_button(self):
        self.ui.create_protocol_button.setEnabled(True)

    def create_protocol(self):
        measure_id = self.get_selected_id()

    def chow_table_custom_menu(self, a_position: QtCore.QPoint):
        menu = QtWidgets.QMenu(self)
        delete_measure_act = menu.addAction("Удалить измерение")
        delete_measure_act.triggered.connect(self.delete_measure)
        menu.popup(self.ui.measures_table.viewport().mapToGlobal(a_position))

    def delete_measure(self):
        reply = QtWidgets.QMessageBox.question(self, "Подтвердите действие", "Вы действительно хотите удалить "
                                               "выбранное измерение?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            measure_id = self.get_selected_id()
            assert measure_id is not None, "measure id must not be None!"

            self.control_db_connection.delete(measure_id)
            self.display_db_model.select()

    def get_selected_id(self):
        selected = self.ui.measures_table.selectionModel().selectedRows()
        if selected:
            selected_row = selected[0].row()
            measure_id = self.sort_proxy_model.index(selected_row, MeasureColumn.ID).data()
            return measure_id
        else:
            return None

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.parent.saveGeometry())
        self.settings.save_header_state(self.__class__.__name__, self.ui.measures_table.horizontalHeader().saveState())
        self.display_db_connection.close()
        self.header_context.delete_connections()
        a_event.accept()
