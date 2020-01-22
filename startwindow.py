from ui.py.startform import Ui_MainWindow as StartForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui, QtWidgets, QtCore

from source_mode_window import SourceModeWindow
from new_no_template_measure_dialog import NewNoTemplateMeasureDialog
from new_no_template_measure_dialog import NoTemplateConfig
from no_template_mode_window import NoTemplateWindow
import clb_dll
import calibrator_constants as clb


class StartWindow(QMainWindow):
    clb_list_changed = pyqtSignal([list])
    usb_status_changed = pyqtSignal(clb.State)

    def __init__(self):
        super().__init__()

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.show()

        self.ui.source_mode_button.clicked.connect(self.source_mode_chosen)
        self.ui.no_template_mode_button.clicked.connect(self.config_no_template_mode)
        self.ui.template_mode_button.clicked.connect(self.template_mode_chosen)

        self.clb_driver = clb_dll.set_up_driver(clb_dll.path)
        self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
        self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
        self.calibrator = clb_dll.ClbDrv(self.clb_driver)
        self.clb_state = clb.State.DISCONNECTED

        self.usb_check_timer = QTimer()
        self.usb_check_timer.timeout.connect(self.usb_tick)
        self.usb_check_timer.start(10)

        self.no_template_config: NoTemplateConfig = None

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

    @pyqtSlot()
    def source_mode_chosen(self):
        try:
            self.hide()
            source_more_window = SourceModeWindow(self.calibrator)
            self.attach_calibrator_to_window(source_more_window)
            source_more_window.exec()
            self.show()
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def config_no_template_mode(self):
        try:
            new_no_template_window = NewNoTemplateMeasureDialog(self.calibrator, self.no_template_config, self)
            new_no_template_window.config_ready.connect(self.save_no_template_config)
            self.attach_calibrator_to_window(new_no_template_window)

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
            self.hide()
            no_template_window = NoTemplateWindow(self.calibrator, self.no_template_config)
            self.attach_calibrator_to_window(no_template_window)
            no_template_window.exec()
            self.show()
        except Exception as err:
            print(err)

    @pyqtSlot()
    def template_mode_chosen(self):
        pass

    def attach_calibrator_to_window(self, a_window):
        assert hasattr(a_window, "update_clb_list"), "no method update_clb_list"
        assert hasattr(a_window, "update_clb_status"), "no method update_clb_status"

        self.clb_list_changed.connect(a_window.update_clb_list)
        self.clb_list_changed.emit(self.usb_driver.get_dev_list())

        self.usb_status_changed.connect(a_window.update_clb_status)
        self.usb_status_changed.emit(self.clb_state)

        # assert self.receivers(self.clb_list_changed) == 1, "clb_list_changed must be connected to only one slot"
        # assert self.receivers(self.usb_status_changed) == 1, "usb_status_changed must be connected to only one slot"
