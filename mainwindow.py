from ui.py.mainform import Ui_MainWindow as MainForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import ctypes

import calibrator_constants as clb


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainForm()
        self.ui.setupUi(self)
        self.show()

        # self.clb_driver = ctypes.cdll.clb_driver_dll
        self.clb_driver = self.set_up_clb_driver_library("C:\\Users\\503\\Desktop\\Qt Projects\\clb_driver_dll\\"
                                                         "build-clb_driver_dll-Desktop_Qt_5_12_2_MSVC2017_32bit-Release"
                                                         "\\release\\clb_driver_dll.dll")

        # Обязательно перед любыми действиями с clb_driver_dll
        self.clb_driver.usb_init()
        print(self.clb_driver.version())

        self.usb_check_timer = QTimer()
        self.usb_check_timer.timeout.connect(self.update_usb)
        self.usb_check_timer.start(10)

        self.connect_signals()

        self.clb_params = clb.ClbParams()
        self.int_to_signal_type = {
            clb.SignalType.ACI: self.ui.aci_radio,
            clb.SignalType.ACV: self.ui.acv_radio,
            clb.SignalType.DCI: self.ui.dci_radio,
            clb.SignalType.DCV: self.ui.dcv_radio,
        }
        self.int_to_mode = {
            clb.Mode.SOURCE: self.ui.source_mode_radio,
            clb.Mode.FIXED_RANGE: self.ui.fixed_mode_radio,
            clb.Mode.DETUNING: self.ui.detuning_radio,
        }
        self.usb_status = clb.UsbState.DISABLED
        self.block_signals = False

    @staticmethod
    def set_up_clb_driver_library(a_full_path):
        clb_driver_lib = ctypes.CDLL(a_full_path)

        # Возвращает список калибраторов, разделенных ';'
        clb_driver_lib.get_usb_devices.restype = ctypes.c_wchar_p

        clb_driver_lib.connect_usb.argtypes = [ctypes.c_wchar_p]

        clb_driver_lib.set_amplitude.argtypes = [ctypes.c_double]
        clb_driver_lib.get_amplitude.restype = ctypes.c_double

        clb_driver_lib.set_frequency.argtypes = [ctypes.c_double]
        clb_driver_lib.get_frequency.restype = ctypes.c_double

        clb_driver_lib.set_signal_type.argtypes = [ctypes.c_int]
        clb_driver_lib.get_signal_type.restype = ctypes.c_int

        clb_driver_lib.set_polarity.argtypes = [ctypes.c_int]
        clb_driver_lib.get_polarity.restype = ctypes.c_int

        clb_driver_lib.signal_enable.argtypes = [ctypes.c_int]
        clb_driver_lib.enabled.restype = ctypes.c_int

        clb_driver_lib.get_usb_status.restype = ctypes.c_int
        clb_driver_lib.is_connected.restype = ctypes.c_int

        clb_driver_lib.set_mode.argtypes = [ctypes.c_int]
        clb_driver_lib.get_mode.restype = ctypes.c_int

        return clb_driver_lib

    def connect_signals(self):
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)
        self.ui.amplitude_spinbox.valueChanged.connect(self.set_amplitude)
        self.ui.frequency_spinbox.valueChanged.connect(self.set_frequency)

        self.ui.polarity_button.clicked.connect(self.polarity_button_clicked)

        self.ui.aci_radio.toggled.connect(self.aci_radio_checked)
        self.ui.acv_radio.toggled.connect(self.acv_radio_checked)
        self.ui.dci_radio.toggled.connect(self.dci_radio_checked)
        self.ui.dcv_radio.toggled.connect(self.dcv_radio_checked)

        self.ui.source_mode_radio.toggled.connect(self.source_radio_checked)
        self.ui.fixed_mode_radio.toggled.connect(self.fixed_radio_checked)
        self.ui.detuning_radio.toggled.connect(self.detuning_radio_checked)

        self.ui.enable_button.clicked.connect(self.signal_enable)

    def update_usb(self):
        self.clb_driver.usb_tick()
        self.clb_driver.clb_tick()
        if self.clb_driver.usb_devices_changed():
            self.ui.clb_list_combobox.clear()

            clb_names_list: str = self.clb_driver.get_usb_devices()
            for clb_name in clb_names_list.split(';'):
                if clb_name:
                    self.ui.clb_list_combobox.addItem(clb_name)

        usb_status = self.clb_driver.get_usb_status()
        if self.usb_status != usb_status:
            self.usb_status = usb_status
            self.ui.usb_state_label.setText(clb.int_to_usb_status[usb_status])

        self.sync_clb_parameters()

    def connect_to_clb(self, a_clb_name):
        if a_clb_name:
            self.clb_driver.connect_usb(a_clb_name)
        else:
            self.clb_driver.disconnect_usb()

    def sync_clb_parameters(self):
        self.block_signals = True

        if self.clb_params.sync_parameter("amplitude", self.clb_driver.get_amplitude()):
            self.ui.amplitude_spinbox.setValue(self.clb_params.amplitude)
        if self.clb_params.sync_parameter("frequency", self.clb_driver.get_frequency()):
            self.ui.frequency_spinbox.setValue(self.clb_params.frequency)
        if self.clb_params.sync_parameter("signal_type", self.clb_driver.get_signal_type()):
            self.int_to_signal_type[self.clb_params.signal_type].setChecked(True)

        if self.clb_params.sync_parameter("dc_polarity", self.clb_driver.get_polarity()):
            self.ui.polarity_button.setText(clb.int_to_polarity[self.clb_params.dc_polarity])
            if self.clb_params.dc_polarity == clb.Polatiry.POS:
                self.ui.polarity_button.setChecked(False)
            else:
                self.ui.polarity_button.setChecked(True)

        if self.clb_params.sync_parameter("signal_on", self.clb_driver.enabled()):
            if self.clb_params.signal_on:
                self.ui.enable_button.setChecked(True)
                self.ui.enable_button.setText("Disable")
            else:
                self.ui.enable_button.setChecked(False)
                self.ui.enable_button.setText("Enable")

        if self.clb_params.sync_parameter("mode", self.clb_driver.get_mode()):
            self.int_to_mode[self.clb_params.mode].setChecked(True)

        self.block_signals = False

    def set_amplitude(self):
        if not self.block_signals:
            amplitude = self.ui.amplitude_spinbox.value()
            self.clb_driver.set_amplitude(amplitude)

    def set_frequency(self):
        if not self.block_signals:
            frequency = self.ui.frequency_spinbox.value()
            self.clb_driver.set_frequency(frequency)

    def polarity_button_clicked(self, a_checked):
        if not self.block_signals:
            if a_checked:
                self.clb_driver.set_polarity(clb.Polatiry.NEG)
                self.ui.polarity_button.setText(clb.int_to_polarity[clb.Polatiry.NEG])
            else:
                self.clb_driver.set_polarity(clb.Polatiry.POS)
                self.ui.polarity_button.setText(clb.int_to_polarity[clb.Polatiry.POS])

    def aci_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_signal_type(clb.SignalType.ACI)

    def acv_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_signal_type(clb.SignalType.ACV)

    def dci_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_signal_type(clb.SignalType.DCI)

    def dcv_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_signal_type(clb.SignalType.DCV)

    def source_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_mode(clb.Mode.SOURCE)

    def fixed_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_mode(clb.Mode.FIXED_RANGE)

    def detuning_radio_checked(self):
        if not self.block_signals:
            self.clb_driver.set_mode(clb.Mode.DETUNING)

    def signal_enable(self, a_enable):
        if not self.block_signals:
            self.clb_driver.signal_enable(a_enable)
