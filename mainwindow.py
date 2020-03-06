from typing import Union

from PyQt5 import QtWidgets, QtCore, QtGui

from new_fast_measure_dialog import NewFastMeasureDialog, FastMeasureParams
from template_list_window import TemplateParams, TemplateListWindow
from variable_template_fields_dialog import VariableTemplateParams
from settings_ini_parser import Settings, BadIniException
from ui.py.mainwindow import Ui_MainWindow as MainForm
from db_measures import Measure, MeasuresDB
from source_mode_window import SourceModeWindow
from settings_dialog import SettingsDialog
from measure_window import MeasureWindow
from startwindow import StartWindow
import calibrator_constants as clb
import clb_dll
import utils


class MainWindow(QtWidgets.QMainWindow):
    clb_list_changed = QtCore.pyqtSignal([list])
    usb_status_changed = QtCore.pyqtSignal(clb.State)

    def __init__(self):
        super().__init__()

        self.ui = MainForm()
        self.ui.setupUi(self)

        self.active_window = None

        try:
            self.settings = Settings(self)
            ini_ok = True
        except BadIniException:
            ini_ok = False
            QtWidgets.QMessageBox.critical(self, "Ошибка", 'Файл конфигурации поврежден. Пожалуйста, '
                                                           'удалите файл "settings.ini" и запустите программу заново')
        if ini_ok:
            self.db_name = "measures.db"
            self.db_connection = MeasuresDB.create_db(self.db_name)
            self.show_start_window()
            self.show()

            self.clb_signal_off_timer = QtCore.QTimer()
            # noinspection PyTypeChecker
            self.clb_signal_off_timer.timeout.connect(self.close)
            self.SIGNAL_OFF_TIME_MS = 200

            self.clb_driver = clb_dll.set_up_driver(clb_dll.path)
            self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
            self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
            self.calibrator = clb_dll.ClbDrv(self.clb_driver)
            self.clb_state = clb.State.DISCONNECTED

            self.usb_check_timer = QtCore.QTimer(self)
            self.usb_check_timer.timeout.connect(self.usb_tick)
            self.usb_check_timer.start(10)

            self.fast_config: Union[FastMeasureParams, None] = None

            self.ui.enter_settings_action.triggered.connect(self.open_settings)

        else:
            self.close()

    def __del__(self):
        if hasattr(self, "display_db_connection"):
            self.db_connection.close()

    def show_start_window(self):
        try:
            self.hide()
            if self.active_window is not None:
                self.active_window.close()

            self.active_window = StartWindow(self.db_connection, self.db_name, self.settings, self)
            self.setCentralWidget(self.active_window)
            self.active_window.source_mode_chosen.connect(self.open_source_mode_window)
            self.active_window.no_template_mode_chosen.connect(self.open_config_no_template_mode)
            self.active_window.template_mode_chosen.connect(self.template_mode_chosen)
            self.setWindowTitle(self.active_window.windowTitle())
        except Exception as err:
            utils.exception_handler(err)

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

    def change_window(self, a_new_window):
        self.active_window = a_new_window
        self.attach_calibrator_to_window(self.active_window)

        self.setCentralWidget(self.active_window)
        self.setWindowTitle(self.active_window.windowTitle())

        self.active_window.close_confirmed.connect(self.close_child_widget)

    def open_source_mode_window(self):
        try:
            self.hide()
            self.active_window.close()
            self.change_window(SourceModeWindow(self.settings, self.calibrator, self))
        except Exception as err:
            utils.exception_handler(err)

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
            measure_config = Measure.fromFastParams(self.fast_config)

            self.hide()
            self.active_window.close()
            self.change_window(MeasureWindow(a_calibrator=self.calibrator,
                                             a_measure_config=measure_config,
                                             a_db_connection=self.db_connection,
                                             a_settings=self.settings,
                                             a_parent=self))
        except Exception as err:
            utils.exception_handler(err)

    def template_mode_chosen(self):
        try:
            template_list_dialog = TemplateListWindow(self.settings, self)
            template_list_dialog.config_ready.connect(self.start_template_measure)
            template_list_dialog.exec()
        except Exception as err:
            utils.exception_handler(err)

    def start_template_measure(self, a_template_params: TemplateParams, a_variable_params: VariableTemplateParams):
        try:
            measure_config = Measure.fromTemplate(a_template_params, a_variable_params)

            self.hide()
            self.active_window.close()
            self.change_window(MeasureWindow(a_calibrator=self.calibrator,
                                             a_measure_config=measure_config,
                                             a_db_connection=self.db_connection,
                                             a_settings=self.settings,
                                             a_parent=self))
        except Exception as err:
            utils.exception_handler(err)

    def close_child_widget(self):
        self.show_start_window()

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.settings, self.db_connection, self)
            settings_dialog.exec()
        except Exception as err:
            utils.exception_handler(err)

    def closeEvent(self, a_event: QtGui.QCloseEvent):
        try:
            if not isinstance(self.active_window, StartWindow):
                if hasattr(self.active_window, "ask_for_close"):
                    # Эмитит close_confirmed при подтверждении закрытия
                    self.active_window.ask_for_close()
                    a_event.ignore()
                else:
                    a_event.accept()
            else:
                if self.calibrator.signal_enable:
                    self.calibrator.signal_enable = False
                    self.clb_signal_off_timer.start(self.SIGNAL_OFF_TIME_MS)
                    a_event.ignore()
                else:
                    self.active_window.close()
                    a_event.accept()
        except Exception as err:
            print(err)
