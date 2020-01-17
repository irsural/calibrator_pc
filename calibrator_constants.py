import enum
from collections import namedtuple

MAX_CURRENT = 11
MIN_CURRENT = -11

MAX_VOLTAGE = 630
MIN_VOLTAGE = -630

MIN_ALTERNATIVE = 0

MAX_FREQUENCY = 2000
MIN_FREQUENCY = 35


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


enum_to_mode = {
    Mode.SOURCE: "Источник",
    Mode.FIXED_RANGE: "Фиксированный",
    Mode.DETUNING: "Расстройка",
}

enum_to_signal_type = {
    SignalType.ACI: "Переменный ток",
    SignalType.ACV: "Переменное напряжение",
    SignalType.DCI: "Постоянный ток",
    SignalType.DCV: "Постоянное напряжение"
}

Step = namedtuple("Step", "ROUGH COMMON EXACT")
AmplitudeStep = Step(0.005, 0.0005, 0.00002)
