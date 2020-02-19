import sqlite3

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtWidgets, QtCore, QtGui

from new_fast_measure_dialog import NewFastMeasureDialog, FastMeasureParams
from variable_template_fields_dialog import VariableTemplateParams
from template_list_window import TemplateParams, TemplateListWindow
from db_measures import MeasureParams, MeasureTables
from ui.py.mainwindow import Ui_MainWindow as MainForm
from measure_window import MeasureWindow
from source_mode_window import SourceModeWindow
from settings_dialog import SettingsDialog
from settings_ini_parser import Settings
from startwindow import StartWindow
import calibrator_constants as clb
import clb_dll
import utils


class MainWindow(QtWidgets.QMainWindow):
    clb_list_changed = pyqtSignal([list])
    usb_status_changed = pyqtSignal(clb.State)

    def __init__(self):
        super().__init__()

        self.ui = MainForm()
        self.ui.setupUi(self)
        self.show()

        self.active_window = None
        self.previous_start_window_pos = self.pos()
        self.show_start_window()

        self.settings = Settings(self)

        self.clb_driver = clb_dll.set_up_driver(clb_dll.path)
        self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
        self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
        self.calibrator = clb_dll.ClbDrv(self.clb_driver)
        self.clb_state = clb.State.DISCONNECTED

        self.usb_check_timer = QtCore.QTimer(self)
        self.usb_check_timer.timeout.connect(self.usb_tick)
        self.usb_check_timer.start(10)

        self.fast_config: FastMeasureParams = None

        self.measure_db_tables = MeasureTables(marks_table="marks", mark_values_table="mark_values",
                                               measures_table="measures", results_table="results")
        self.db_connection = self.create_db("measures.db")

        self.clb_signal_off_timer = QtCore.QTimer()
        self.clb_signal_off_timer.timeout.connect(self.close)
        self.SIGNAL_OFF_TIME_MS = 200

        self.ui.enter_settings_action.triggered.connect(self.open_settings)

    def __del__(self):
        if hasattr(self, "db_connection"):
            self.db_connection.close()

    def create_db(self, a_db_name: str):
        connection = sqlite3.connect(a_db_name)
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.measure_db_tables.marks_table} "
                           f"(name text primary key, tag text unique, default_value text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.measure_db_tables.measures_table} "
                           f"(id integer primary key autoincrement, organisation text, etalon_device text,"
                           f"device_name text, device_creator text, device_system integer, signal_type integer,"
                           f"device_class real, serial_number text, owner text, user text, date text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.measure_db_tables.mark_values_table} "
                           f"(id integer primary key autoincrement, value text, mark_name text,  measure_id int, "
                           f"unique (mark_name, measure_id), "
                           f"foreign key (mark_name) references {self.measure_db_tables.marks_table}(name),"
                           f"foreign key (measure_id) references {self.measure_db_tables.measures_table}(id))")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.measure_db_tables.results_table} "
                           f"(id integer primary key autoincrement, point real, frequency real, up_value real,"
                           f"up_deviation real, up_deviation_percent real, down_value real, down_deviation real,"
                           f"down_deviation_percent real, variation real, measure_id int,"
                           f"foreign key (measure_id) references {self.measure_db_tables.measures_table}(id))")
        return connection

    def show_start_window(self):
        try:
            if self.active_window is not None:
                self.active_window.close()
            self.active_window = StartWindow(self)
            self.resize(self.active_window.width(), self.active_window.height())
            self.setCentralWidget(self.active_window)
            self.active_window.source_mode_chosen.connect(self.open_source_mode_window)
            self.active_window.no_template_mode_chosen.connect(self.open_config_no_template_mode)
            self.active_window.template_mode_chosen.connect(self.template_mode_chosen)
            self.setWindowTitle(self.active_window.windowTitle())
            self.move(self.previous_start_window_pos)
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def usb_tick(self):
        self.usb_driver.tick()

        if self.usb_driver.is_dev_list_changed():
            self.clb_list_changed.emit(self.usb_driver.get_dev_list())

        if self.usb_driver.is_status_changed():
            self.usb_state = self.usb_driver.get_status()

        current_state = clb.State.DISCONNECTED
        if self.usb_state == clb_dll.UsbDrv.UsbState.CONNECTED:
            self.calibrator.signal_enable_changed()

            if not self.calibrator.signal_enable:
                current_state = clb.State.STOPPED
            elif not self.calibrator.is_signal_ready():
                current_state = clb.State.WAITING_SIGNAL
            else:
                current_state = clb.State.READY

        if self.clb_state != current_state:
            self.clb_state = current_state
            self.usb_status_changed.emit(self.clb_state)

    def attach_calibrator_to_window(self, a_window):
        assert hasattr(a_window, "update_clb_list"), "no method update_clb_list"
        assert hasattr(a_window, "update_clb_status"), "no method update_clb_status"

        self.clb_list_changed.connect(a_window.update_clb_list)
        self.clb_list_changed.emit(self.usb_driver.get_dev_list())

        self.usb_status_changed.connect(a_window.update_clb_status)
        self.usb_status_changed.emit(self.clb_state)

    @staticmethod
    def sync_centers(a_old_widget, a_new_widget):
        new_center: QtCore.QPoint = a_old_widget.geometry().center() - a_new_widget.rect().center()
        new_center.setY(utils.bound(new_center.y(), 0, QtWidgets.QApplication.desktop().screenGeometry().height() -
                                    a_new_widget.height()))
        return new_center

    def change_window(self, a_new_window):
        self.previous_start_window_pos = self.pos()
        self.active_window.close()
        self.active_window = a_new_window
        self.attach_calibrator_to_window(self.active_window)

        self.move(self.sync_centers(self, self.active_window))
        self.resize(self.active_window.size())
        self.setCentralWidget(self.active_window)

        self.setWindowTitle(self.active_window.windowTitle())

        self.active_window.close_confirmed.connect(self.close_child_widget)

    @pyqtSlot()
    def open_source_mode_window(self):
        try:
            self.change_window(SourceModeWindow(self.calibrator, self))
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def open_config_no_template_mode(self):
        try:
            new_fast_measure_window = NewFastMeasureDialog(self.fast_config, self)
            new_fast_measure_window.config_ready.connect(self.save_no_template_config)

            if new_fast_measure_window.exec() == QtWidgets.QDialog.Accepted:
                assert self.fast_config is not None, "no_template_config must not be None!"
                new_fast_measure_window.close()
                self.start_fast_measure()
        except AssertionError as err:
            print(err)

    def save_no_template_config(self, a_config: FastMeasureParams):
        self.fast_config = a_config

    def start_fast_measure(self):
        try:
            measure_config = MeasureParams.fromFastParams(self.fast_config)
            self.change_window(MeasureWindow(a_calibrator=self.calibrator,
                                             a_measure_config=measure_config,
                                             a_db_connection=self.db_connection,
                                             a_db_tables=self.measure_db_tables,
                                             a_settings=self.settings,
                                             a_parent=self))
        except Exception as err:
            utils.exception_handler(err)

    @pyqtSlot()
    def template_mode_chosen(self):
        try:
            template_list_dialog = TemplateListWindow(self)
            template_list_dialog.config_ready.connect(self.start_template_measure)
            template_list_dialog.exec()
        except Exception as err:
            utils.exception_handler(err)

    def start_template_measure(self, a_template_params: TemplateParams, a_variable_params: VariableTemplateParams):
        try:
            measure_config = MeasureParams.fromTemplate(a_template_params, a_variable_params)
            self.change_window(MeasureWindow(a_calibrator=self.calibrator,
                                             a_measure_config=measure_config,
                                             a_db_connection=self.db_connection,
                                             a_db_tables=self.measure_db_tables,
                                             a_settings=self.settings,
                                             a_parent=self))
        except Exception as err:
            utils.exception_handler(err)

    def close_child_widget(self):
        self.show_start_window()

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.settings, self.db_connection, self.measure_db_tables, self)
            settings_dialog.exec()
        except Exception as err:
            utils.exception_handler(err)

    def closeEvent(self, a_event: QtGui.QCloseEvent):
        try:
            if not isinstance(self.active_window, StartWindow):
                assert hasattr(self.active_window, "ask_for_close"), \
                    f"Class {type(self.active_window)} has no method ask_for_close"
                # Эмитит close_confirmed при подтверждении закрытия
                self.active_window.ask_for_close()
                a_event.ignore()
            else:
                if self.calibrator.signal_enable:
                    self.calibrator.signal_enable = False
                    self.clb_signal_off_timer.start(self.SIGNAL_OFF_TIME_MS)
                    a_event.ignore()
        except AssertionError as err:
            print(err)
