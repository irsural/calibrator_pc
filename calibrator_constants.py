import enum


class UsbState(enum.IntEnum):
    NOT_SUPPORTED = 0
    DISABLED = 1
    CONNECTED = 2
    BUSY = 3
    ERROR = 4


class DcPolatiry(enum.IntEnum):
    POS = 0
    NEG = 1


class SignalType(enum.IntEnum):
    ACI = 0
    ACV = 1
    DCI = 2
    DCV = 3


class ClbParams:
    def __init__(self):
        self.amplitude = 0
        self.frequency = 40
        self.signal_type = SignalType.ACI
        self.dc_polarity = DcPolatiry.POS
        self.signal_on = False

    def sync_parameter(self, param_name: str, value):
        variable = getattr(self, param_name)
        if variable != value:
            setattr(self, param_name, value)
            return True
        else:
            return False


