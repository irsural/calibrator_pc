from ui.py.mainform import Ui_MainWindow as MainForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import ctypes


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

    @staticmethod
    def set_up_clb_driver_library(a_full_path):
        clb_driver_lib = ctypes.CDLL(a_full_path)

        # Возвращает список калибраторов, разделенных ';'
        clb_driver_lib.get_usb_devices.restype = ctypes.c_wchar_p

        clb_driver_lib.connect_usb.argtypes = [ctypes.c_wchar_p]
        clb_driver_lib.set_amplitude.argtypes = [ctypes.c_double]

        return clb_driver_lib

    def connect_signals(self):
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)
        self.ui.amplitude_spinbox.valueChanged.connect(self.set_amplitude)

    def update_usb(self):
        self.clb_driver.usb_tick()
        if self.clb_driver.usb_devices_changed():
            self.ui.clb_list_combobox.clear()

            clb_names_list: str = self.clb_driver.get_usb_devices()
            for clb_name in clb_names_list.split(';'):
                if clb_name:
                    self.ui.clb_list_combobox.addItem(clb_name)

    def connect_to_clb(self, a_clb_name):
        if a_clb_name:
            print(self.clb_driver.connect_usb(a_clb_name))
        else:
            self.clb_driver.disconnect_usb()

    def set_amplitude(self):
        amplitude = self.ui.amplitude_spinbox.value()
        self.clb_driver.set_amplitude(amplitude)
