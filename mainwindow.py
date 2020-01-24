import configparser
import os

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtWidgets, QtCore, QtGui

from new_no_template_measure_dialog import NewNoTemplateMeasureDialog, NoTemplateConfig
from ui.py.mainwindow import Ui_MainWindow as MainForm
from no_template_mode_window import NoTemplateWindow
from source_mode_window import SourceModeWindow
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
        self.show_start_window()

        self.settings = self.restore_settings(cfg.CONFIG_PATH)

        self.clb_driver = clb_dll.set_up_driver(clb_dll.path)
        self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
        self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
        self.calibrator = clb_dll.ClbDrv(self.clb_driver)
        self.clb_state = clb.State.DISCONNECTED

        self.usb_check_timer = QtCore.QTimer()
        self.usb_check_timer.timeout.connect(self.usb_tick)
        self.usb_check_timer.start(10)

        self.no_template_config: NoTemplateConfig = None

    @staticmethod
    def restore_settings(a_path: str):
        settings = configparser.ConfigParser()

        if not os.path.exists(a_path):
            settings[cfg.NO_TEMPLATE_SECTION] = {cfg.FIXED_RANGES_KEY: "0.0001,0.01,0.1,1,10,20,100"}

            with open(a_path, 'w') as config_file:
                settings.write(config_file)
        else:
            settings.read(a_path)

        # Выводит ini файл в консоль
        # for key in settings:
        #     print(f"[{key}]")
        #     for subkey in settings[key]:
        #         print(f"{subkey} = {settings[key][subkey]}")

        return settings

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
            self.move(self.sync_centers(self, self.active_window))
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
        if not self.usb_state == clb_dll.UsbDrv.UsbState.DISABLED:
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

    def sync_centers(self, a_old_widget, a_new_widget):
        new_center: QtCore.QPoint = a_old_widget.geometry().center() - a_new_widget.rect().center()
        new_center.setY(utils.bound(new_center.y(), 0, QtWidgets.QApplication.desktop().screenGeometry().height() -
                                    a_new_widget.height()))
        return new_center

    def change_window(self, a_new_window):
        self.active_window.close()
        self.active_window = a_new_window
        self.attach_calibrator_to_window(self.active_window)
        self.setCentralWidget(self.active_window)
        self.ui.back_action.triggered.connect(self.show_start_window)
        self.move(self.sync_centers(self, self.active_window))

    @pyqtSlot()
    def open_source_mode_window(self):
        try:
            self.change_window(SourceModeWindow(self.calibrator, self))
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def open_config_no_template_mode(self):
        try:
            new_no_template_window = NewNoTemplateMeasureDialog(self.calibrator, self.no_template_config, self)
            self.attach_calibrator_to_window(new_no_template_window)
            new_no_template_window.config_ready.connect(self.save_no_template_config)

            if new_no_template_window.exec() == QtWidgets.QDialog.Accepted:
                assert self.no_template_config is not None, "no_template_config must not be None!"
                new_no_template_window.close()
                self.no_template_mode_chosen()
        except AssertionError as err:
            print(err)

    def save_no_template_config(self, a_config: NoTemplateConfig):
        self.no_template_config = a_config

    def no_template_mode_chosen(self):
        try:
            self.change_window(NoTemplateWindow(self.calibrator, self.no_template_config, self.settings, self))
            self.ui.change_fixed_range_action.triggered.connect(self.active_window.edit_fixed_step)
        except Exception as err:
            print(err)

    @pyqtSlot()
    def template_mode_chosen(self):
        pass

    # def closeEvent(self, a_event: QtGui.QCloseEvent):
    #     if isinstance(self.active_window, NoTemplateWindow):
    #         self.active_window.close()
    #         a_event.ignore()


