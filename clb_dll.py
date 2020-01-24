import ctypes
import enum

import calibrator_constants as clb
import utils


path = "C:\\Users\\503\\Desktop\\Qt Projects\\clb_driver_dll\\" \
       "build-clb_driver_dll-Desktop_Qt_5_12_2_MSVC2017_32bit-Release\\release\\clb_driver_dll.dll"


def set_up_driver(a_full_path):
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

    clb_driver_lib.is_signal_ready.restype = ctypes.c_int

    return clb_driver_lib


class UsbDrv:
    class UsbState(enum.IntEnum):
        NOT_SUPPORTED = 0
        DISABLED = 1
        CONNECTED = 2
        BUSY = 3
        ERROR = 4

    # enum_to_usb_status = {
    #     UsbState.DISABLED: "Отключено",
    #     UsbState.BUSY: "Подключение...",
    #     UsbState.CONNECTED: "Подключено",
    #     UsbState.ERROR: "Ошибка",
    #     UsbState.NOT_SUPPORTED: "",
    # }

    def __init__(self, a_clb_dll):
        self.clb_dll = a_clb_dll
        # Обязательно перед любыми действиями с clb_driver_dll
        self.clb_dll.usb_init()

        self.clb_dev_list_changed = False
        self.clb_dev_list = []
        self.usb_status_changed = False
        self.usb_status = self.UsbState.DISABLED

    def tick(self):
        self.clb_dll.usb_tick()
        if self.clb_dll.usb_devices_changed():
            self.clb_dev_list.clear()

            clb_names_list: str = self.clb_dll.get_usb_devices()
            for clb_name in clb_names_list.split(';'):
                if clb_name:
                    self.clb_dev_list.append(clb_name)
            self.clb_dev_list_changed = True

        usb_status = self.clb_dll.get_usb_status()
        if self.usb_status != usb_status:
            self.usb_status = usb_status
            self.usb_status_changed = True

    def is_status_changed(self):
        if self.usb_status_changed:
            self.usb_status_changed = False
            return True
        else:
            return False

    def is_dev_list_changed(self):
        if self.clb_dev_list_changed:
            self.clb_dev_list_changed = False
            return True
        else:
            return False

    def get_dev_list(self):
        return self.clb_dev_list

    def get_status(self):
        return self.UsbState(self.usb_status)


class ClbDrv:
    def __init__(self, a_clb_dll):
        self.__clb_dll = a_clb_dll

        self.__amplitude = 0
        self.__frequency = 0
        self.__signal_type = clb.SignalType.ACI
        self.__dc_polarity = clb.Polatiry.POS
        self.__signal_on = False
        self.__mode = clb.Mode.SOURCE
        self.__signal_ready = False

    def connect(self, a_clb_name: str):
        # Костыль чтобы частота не сбрасывалась при реконнекте калибратора
        # self.__frequency = 0
        if a_clb_name:
            self.__clb_dll.connect_usb(a_clb_name)
        else:
            self.__clb_dll.disconnect_usb()

    def amplitude_changed(self):
        actual_amplitude = self.__clb_dll.get_amplitude()
        signed_amplitude = actual_amplitude if self.__clb_dll.get_polarity() == clb.Polatiry.POS else -actual_amplitude

        if self.__amplitude != signed_amplitude:
            self.__amplitude = signed_amplitude
            return True
        else:
            return False

    @property
    def amplitude(self):
        return self.__amplitude

    @amplitude.setter
    def amplitude(self, a_amplitude: float):
        self.__amplitude = self.__bound_amplitude(a_amplitude)
        self.__clb_dll.set_amplitude(abs(self.__amplitude))
        self.__set_polarity_by_amplitude_sign(self.__amplitude)

    def __bound_amplitude(self, a_amplitude):
        min_value = clb.MIN_VOLTAGE
        max_value = clb.MAX_VOLTAGE
        if self.__signal_type == clb.SignalType.ACI or self.__signal_type == clb.SignalType.DCI:
            min_value = clb.MIN_CURRENT
            max_value = clb.MAX_CURRENT
        if self.__signal_type == clb.SignalType.ACV or self.__signal_type == clb.SignalType.ACI:
            min_value = clb.MIN_ALTERNATIVE

        return utils.bound(a_amplitude, min_value, max_value)

    def __set_polarity_by_amplitude_sign(self, a_amplitude):
        if a_amplitude < 0 and self.__clb_dll.get_polarity() != clb.Polatiry.NEG:
            self.__clb_dll.set_polarity(clb.Polatiry.NEG)
        elif a_amplitude >= 0 and self.__clb_dll.get_polarity() != clb.Polatiry.POS:
            self.__clb_dll.set_polarity(clb.Polatiry.POS)

    def frequency_changed(self):
        actual_frequency = self.__clb_dll.get_frequency()
        if self.__frequency != actual_frequency:
            self.__frequency = actual_frequency
            return True
        else:
            return False

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, a_frequency: float):
        self.__frequency = utils.bound(a_frequency, clb.MIN_FREQUENCY, clb.MAX_FREQUENCY)
        self.__clb_dll.set_frequency(a_frequency)

    def signal_type_changed(self):
        actual_signal_type = self.__clb_dll.get_signal_type()
        if self.__signal_type != actual_signal_type:
            self.__signal_type = actual_signal_type
            return True
        else:
            return False

    @property
    def signal_type(self):
        return self.__signal_type

    @signal_type.setter
    def signal_type(self, a_signal_type: int):
        self.__signal_type = a_signal_type
        self.__clb_dll.set_signal_type(a_signal_type)

    def is_signal_ready(self):
        return self.__clb_dll.is_signal_ready()

    # def polarity_changed(self):
    #     actual_polarity = self.__clb_dll.get_polarity()
    #     if self.__dc_polarity != actual_polarity:
    #         self.__set_amplitude_sign(actual_polarity)
    #         print(2, self.amplitude)
    #         self.__dc_polarity = actual_polarity
    #         print(3, self.__dc_polarity)
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def polarity(self):
    #     return self.__dc_polarity
    #
    # @polarity.setter
    # def polarity(self, a_polarity: int):
    #     self.__set_amplitude_sign(a_polarity)
    #     self.__dc_polarity = a_polarity
    #     self.__clb_dll.set_polarity(a_polarity)
    #
    # def __set_amplitude_sign(self, a_polarity):
    #     if a_polarity == clb.Polatiry.POS:
    #         self.__amplitude = abs(self.__amplitude)
    #     elif a_polarity == clb.Polatiry.NEG:
    #         self.__amplitude = -abs(self.__amplitude)

    def signal_enable_changed(self):
        actual_enabled = self.__clb_dll.enabled()
        if self.__signal_on != actual_enabled:
            self.__signal_on = actual_enabled
            return True
        else:
            return False

    @property
    def signal_enable(self):
        return self.__signal_on

    @signal_enable.setter
    def signal_enable(self, a_signal_enable: int):
        self.__signal_on = a_signal_enable
        self.__clb_dll.signal_enable(a_signal_enable)

    def mode_changed(self):
        actual_mode = self.__clb_dll.get_mode()
        if self.__mode != actual_mode:
            self.__mode = actual_mode
            return True
        else:
            return False

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, a_mode: int):
        self.__mode = a_mode
        self.__clb_dll.set_mode(a_mode)

