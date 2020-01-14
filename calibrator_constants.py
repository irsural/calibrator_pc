import enum


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


# class ClbParams:
#     def __init__(self):
#         self.amplitude = 0
#         self.frequency = 0
#         self.signal_type = SignalType.ACI
#         self.dc_polarity = Polatiry.POS
#         self.signal_on = False
#         self.mode = Mode.SOURCE
#
#     def sync_parameter(self, param_name: str, value):
#         variable = getattr(self, param_name)
#         if variable != value:
#             setattr(self, param_name, value)
#             return True
#         else:
#             return False


