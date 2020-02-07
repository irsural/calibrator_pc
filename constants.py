from enum import IntEnum

CONFIG_PATH = "./settings.ini"

NO_TEMPLATE_SECTION = "NoTemplateMode"
FIXED_RANGES_KEY = "fixed_ranges"

COPY_ICON_PATH = "./resources/icons/copy.png"
PLAY_ICON_PATH = "./resources/icons/play.png"
PAUSE_ICON_PATH = "./resources/icons/pause.png"
WARNING_GIF_PATH = "./resources/gif/warning.gif"

FLOAT_EPSILON = 1e-9


class DeviceSystem(IntEnum):
    MAGNETOELECTRIC = 0
    ELECTRODYNAMIC = 1
    ELECTROMAGNETIC = 2


enum_to_device_system = {
    DeviceSystem.MAGNETOELECTRIC: "Магнитоэлектрическая",
    DeviceSystem.ELECTRODYNAMIC: "Электродинамическая",
    DeviceSystem.ELECTROMAGNETIC: "Электромагнитная",
}
