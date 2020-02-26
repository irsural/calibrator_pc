from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore, QtSql

from ui.py.startform import Ui_Form as StartForm
from db_measures import MeasureTables, MeasureColumn, MEASURE_COLUMN_TO_NAME
from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from settings_ini_parser import Settings
import qt_utils


class StartWindow(QtWidgets.QWidget):
    source_mode_chosen = pyqtSignal()
    no_template_mode_chosen = pyqtSignal()
    template_mode_chosen = pyqtSignal()

    def __init__(self, a_db_name: str, a_db_tables: MeasureTables, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.settings = a_settings

        self.setWindowTitle("Калибратор N4-25")

        self.ui.source_mode_button.clicked.connect(self.source_mode_chosen)
        self.ui.no_template_mode_button.clicked.connect(self.no_template_mode_chosen)
        self.ui.template_mode_button.clicked.connect(self.template_mode_chosen)

        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.parent.show()
        # По каким то причинам restoreGeometry не восстанавливает размер MainWindow, если оно скрыто
        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        self.db_connection, self.db_model, self.header_context = \
            self.config_measure_table(a_db_name, a_db_tables.measures_table)

    def config_measure_table(self, a_db_name: str, a_table_name: str):
        db_connection = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_connection.setDatabaseName(a_db_name)

        res = db_connection.open()
        assert res, f"Can't open database {a_db_name}!"

        db_model = QtSql.QSqlTableModel(self)
        db_model.setTable(a_table_name)

        for column in range(db_model.columnCount()):
            db_model.setHeaderData(column, QtCore.Qt.Horizontal, MEASURE_COLUMN_TO_NAME[column])

        sort_filter = QtCore.QSortFilterProxyModel(self)
        sort_filter.setSourceModel(db_model)

        self.ui.measures_table.setModel(sort_filter)
        # Чтобы был приятный цвет выделения
        self.ui.measures_table.setItemDelegate(NonOverlappingDoubleClick(self))

        self.ui.measures_table.horizontalHeader().restoreState(self.settings.get_last_header_state(
            self.__class__.__name__))
        self.ui.measures_table.setColumnHidden(MeasureColumn.ID, True)

        header_context = qt_utils.TableHeaderContextMenu(self, self.ui.measures_table, True)

        db_model.select()

        return db_connection, db_model, header_context

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.parent.saveGeometry())
        self.settings.save_header_state(self.__class__.__name__, self.ui.measures_table.horizontalHeader().saveState())
        self.db_connection.close()
        self.header_context.delete_connections()
        a_event.accept()
