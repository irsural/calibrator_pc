from enum import IntEnum
from collections import namedtuple
from typing import List

from calibrator_constants import SignalType, is_dc_signal

COPY_ICON_PATH = "./resources/icons/copy.png"
PLAY_ICON_PATH = "./resources/icons/play.png"
PAUSE_ICON_PATH = "./resources/icons/pause.png"
PLUS_ICON_PATH = "./resources/icons/plus.png"
MINUS_ICON_PATH = "./resources/icons/minus.png"
WARNING_GIF_PATH = "./resources/gif/warning.gif"
CLOSE_ICON_PATH = "./resources/icons/close.png"
SETTINGS_ICON_PATH = "./resources/icons/settings.png"

FLOAT_EPSILON = 1e-9


MeasuredPoint = namedtuple("Point", ["scale_point", "amplitude", "frequency", "up_value", "down_value"])
Mark = namedtuple("Mark", ["description", "mark", "value"])


class DeviceSystem(IntEnum):
    MAGNETOELECTRIC = 0
    ELECTRODYNAMIC = 1
    ELECTROMAGNETIC = 2


enum_to_device_system = {
    DeviceSystem.MAGNETOELECTRIC: "Магнитоэлектрическая",
    DeviceSystem.ELECTRODYNAMIC: "Электродинамическая",
    DeviceSystem.ELECTROMAGNETIC: "Электромагнитная",
}


class OperationDB(IntEnum):
    ADD = 0
    EDIT = 1


class Scale:
    class Limit:
        def __init__(self, a_id=0, a_limit: float = 1, a_device_class: float = 1,
                     a_signal_type: SignalType = SignalType.ACI, a_frequency: str = ""):
            self.id = a_id
            self.limit = a_limit
            self.device_class = a_device_class
            self.signal_type = a_signal_type

            if a_frequency is not None:
                self.frequency = a_frequency
            elif is_dc_signal[a_signal_type]:
                self.frequency = "0"
            else:
                self.frequency = "50"

        def __str__(self):
            return f"{self.limit}, {self.signal_type}, {self.device_class}"

    def __init__(self, a_id=0, a_number=1, a_scale_points: List[float] = None, a_limits: List[Limit] = None):
        self.id = a_id
        self.number = a_number
        self.points: List[float] = a_scale_points if a_scale_points is not None else []
        self.limits: List[Scale.Limit] = a_limits if a_limits is not None else [Scale.Limit()]

    def __str__(self):
        return f"Points: {self.points}\nLimits: {[str(lim) for lim in self.limits]}"

