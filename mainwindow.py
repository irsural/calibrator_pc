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
        self.clb_driver = ctypes.CDLL("C:\\Users\\503\\Desktop\\Qt Projects\\clb_driver_dll\\"
                                      "build-clb_driver_dll-Desktop_Qt_5_12_2_MSVC2017_32bit-Release\\release\\"
                                      "clb_driver_dll.dll")
        self.clb_driver_get_name = self.clb_driver.usb_info_get_devices
        # Возвращает список калибраторов, разделенных ';'
        self.clb_driver_get_name.restype = ctypes.c_wchar_p
        print(self.clb_driver.version())

        self.usb_check_timer = QTimer()
        self.usb_check_timer.timeout.connect(self.update_usb)
        self.usb_check_timer.start(10)

    def update_usb(self):
        self.clb_driver.usb_info_tick()
        if self.clb_driver.usb_info_changed():
            self.ui.clb_list_combobox.clear()
            
            clb_names_list: str = self.clb_driver_get_name()
            for clb_name in clb_names_list.split(';'):
                if clb_name:
                    self.ui.clb_list_combobox.addItem(clb_name)
