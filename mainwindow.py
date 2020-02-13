import sqlite3
import configparser
import os

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtCore, QtGui

from new_no_template_measure_dialog import NewFastMeasureDialog, FastMeasureParams
from ui.py.mainwindow import Ui_MainWindow as MainForm
from measure_window import MeasureWindow
from template_list_window import TemplateListWindow
from source_mode_window import SourceModeWindow
from settings_dialog import SettingsDialog
from startwindow import StartWindow
import calibrator_constants as clb
import constants as cfg
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

        self.settings = self.restore_settings(cfg.CONFIG_PATH)

        self.clb_driver = clb_dll.set_up_driver(clb_dll.path)
        self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
        self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
        self.calibrator = clb_dll.ClbDrv(self.clb_driver)
        self.clb_state = clb.State.DISCONNECTED

        self.usb_check_timer = QtCore.QTimer(self)
        self.usb_check_timer.timeout.connect(self.usb_tick)
        self.usb_check_timer.start(10)

        self.no_template_config: FastMeasureParams = None

        self.marks_table = "marks"
        self.mark_values_table = "mark_values"
        self.measures_table = "measures"
        self.results_table = "results"
        self.db_connection = self.create_db("measures.db")

        self.clb_signal_off_timer = QtCore.QTimer()
        self.clb_signal_off_timer.timeout.connect(self.close)
        self.SIGNAL_OFF_TIME_MS = 200

        self.ui.enter_settings_action.triggered.connect(self.open_settings)

    def __del__(self):
        self.db_connection.close()

    @staticmethod
    def restore_settings(a_path: str):
        settings = configparser.ConfigParser()

        if not os.path.exists(a_path):
            settings[cfg.NO_TEMPLATE_SECTION] = {cfg.FIXED_RANGES_KEY: "0.0001,0.01,0.1,1,10,20,100"}
            utils.save_settings(a_path, settings)
        else:
            settings.read(a_path)

        # Выводит ini файл в консоль
        # for key in settings:
        #     print(f"[{key}]")
        #     for subkey in settings[key]:
        #         print(f"{subkey} = {settings[key][subkey]}")

        return settings

    def create_db(self, a_db_name: str):
        connection = sqlite3.connect(a_db_name)
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.marks_table} "
                           f"(name text primary key, tag text unique, default_value text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.measures_table} "
                           f"(id integer primary key autoincrement, organisation text, etalon_device text,"
                           f"device_name text, device_creator text, device_system integer, signal_type integer,"
                           f"device_class real, serial_number text, owner text, user text, date text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.mark_values_table} "
                           f"(id integer primary key autoincrement, value text, mark_name text,  measure_id int,"
                           f"foreign key (mark_name) references {self.marks_table}(name),"
                           f"foreign key (measure_id) references {self.measures_table}(id))")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.results_table} "
                           f"(id integer primary key autoincrement, point real, frequency real, up_value real,"
                           f"up_deviation real, up_deviation_percent real, down_value real, down_deviation real,"
                           f"down_deviation_percent real, variation real, measure_id int,"
                           f"foreign key (measure_id) references {self.measures_table}(id))")
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

        # assert self.receivers(self.clb_list_changed) == 1, "clb_list_changed must be connected to only one slot"
        # assert self.receivers(self.usb_status_changed) == 1, "usb_status_changed must be connected to only one slot"

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
            new_no_template_window = NewFastMeasureDialog(self.calibrator, self.no_template_config, self)
            self.attach_calibrator_to_window(new_no_template_window)
            new_no_template_window.config_ready.connect(self.save_no_template_config)

            if new_no_template_window.exec() == QtWidgets.QDialog.Accepted:
                assert self.no_template_config is not None, "no_template_config must not be None!"
                new_no_template_window.close()
                self.no_template_mode_chosen()
        except AssertionError as err:
            print(err)

    def save_no_template_config(self, a_config: FastMeasureParams):
        self.no_template_config = a_config

    def no_template_mode_chosen(self):
        try:
            self.change_window(MeasureWindow(self.calibrator, self.no_template_config, self.settings, self))
            self.ui.change_fixed_range_action.triggered.connect(self.active_window.edit_fixed_step)
        except Exception as err:
            print(err)

    @pyqtSlot()
    def template_mode_chosen(self):
        try:
            template_list_dialog = TemplateListWindow(self)
            if template_list_dialog.exec() == QtWidgets.QDialog.Accepted:
                pass
        except Exception as err:
            print(err)

    def close_child_widget(self):
        # self.active_window.close()
        self.show_start_window()

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.db_connection, self.marks_table, self.mark_values_table, self)
            settings_dialog.exec()
        except Exception as err:
            print(err)

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
