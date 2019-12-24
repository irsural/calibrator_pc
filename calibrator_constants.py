import enum


class UsbState(enum.IntEnum):
    NOT_SUPPORTED = 0
    DISABLED = 1
    CONNECTED = 2
    BUSY = 3
    ERROR = 4


int_to_usb_status = {
    UsbState.DISABLED: "Отключено",
    UsbState.BUSY: "Подключение...",
    UsbState.CONNECTED: "Подключено",
    UsbState.ERROR: "Ошибка",
    UsbState.NOT_SUPPORTED: "",
}


class Polatiry(enum.IntEnum):
    POS = 0
    NEG = 1


int_to_polarity = {
    Polatiry.POS: "+",
    Polatiry.NEG: "-"
}


class SignalType(enum.IntEnum):
    ACI = 0
    ACV = 1
    DCI = 2
    DCV = 3


class Mode(enum.IntEnum):
    SOURCE = 0
    FIXED_RANGE = 1
    DETUNING = 2


int_to_mode = {
    Mode.SOURCE: "Источник",
    Mode.FIXED_RANGE: "Фиксированный",
    Mode.DETUNING: "Расстройка",
}


class ClbParams:
    def __init__(self):
        self.amplitude = 0
        self.frequency = 0
        self.signal_type = SignalType.ACI
        self.dc_polarity = Polatiry.POS
        self.signal_on = False
        self.mode = Mode.SOURCE

    def sync_parameter(self, param_name: str, value):
        variable = getattr(self, param_name)
        if variable != value:
            setattr(self, param_name, value)
            return True
        else:
            return False


