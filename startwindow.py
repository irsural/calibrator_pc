from ui.py.startform import Ui_MainWindow as StartForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QTimer

from source_mode_window import SourceModeWindow
from new_no_template_measure_dialog import NewNoTemplateMeasureDialog
from no_template_mode_window import NoTemplateWindow
import clb_dll
import calibrator_constants as clb


class StartWindow(QMainWindow):
    clb_list_changed = pyqtSignal([list])
    usb_status_changed = pyqtSignal([str])

    def __init__(self):
        super().__init__()

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.setFixedSize(370, 260)
        self.show()

        self.active_window = None

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
            self.usb_status_changed.emit(clb.enum_to_state[self.clb_state])

    @pyqtSlot()
    def source_mode_chosen(self):
        try:
            assert self.active_window is None, "self.active_window must be None before assigment!"
            self.active_window = SourceModeWindow(self.calibrator)
            self.hide()
            self.change_window()

        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def config_no_template_mode(self):
        try:
            assert self.active_window is None, "self.active_window must be None before assigment!"
            self.active_window = NewNoTemplateMeasureDialog(self.calibrator)
            self.active_window.accepted.connect(self.no_template_mode_chosen)
            self.active_window.rejected.connect(self.child_window_closed)
            self.change_window()

        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def no_template_mode_chosen(self):
        self.active_window.accepted.disconnect(self.no_template_mode_chosen)
        try:
            assert hasattr(self.active_window, "get_config"), "no method get_config"
            measure_config = self.active_window.get_config()
            self.child_window_closed()

            assert self.active_window is None, "self.active_window must be None before assigment!"
            self.active_window = NoTemplateWindow(self.calibrator, measure_config)
            self.change_window()

        except Exception as err:
            print(err)

    @pyqtSlot()
    def template_mode_chosen(self):
        pass

    def change_window(self):
        assert hasattr(self.active_window, "window_is_closed"), "no method window_is_closed"
        assert hasattr(self.active_window, "update_clb_list"), "no method update_clb_list"
        assert hasattr(self.active_window, "update_clb_status"), "no method update_clb_status"

        self.active_window.show()

        self.active_window.window_is_closed.connect(self.child_window_closed)

        self.clb_list_changed.connect(self.active_window.update_clb_list)
        self.clb_list_changed.emit(self.usb_driver.get_dev_list())

        self.usb_status_changed.connect(self.active_window.update_clb_status)
        self.usb_status_changed.emit(clb.enum_to_state[self.clb_state])

    @pyqtSlot()
    def child_window_closed(self):
        print("here2")
        try:
            assert self.active_window is not None, "self.active_window must not be None!"
            self.show()
            self.active_window.window_is_closed.disconnect(self.child_window_closed)
            self.clb_list_changed.disconnect(self.active_window.update_clb_list)
            self.usb_status_changed.disconnect(self.active_window.update_clb_status)
            self.active_window = None
        except AssertionError as err:
            print(err)



