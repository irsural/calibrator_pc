import configparser
import os
from typing import List
from enum import IntEnum

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

import utils


class BadIniException(Exception):
    pass


class Settings(QtCore.QObject):
    CONFIG_PATH = "./settings.ini"

    class ValueType(IntEnum):
        INT = 0
        FLOAT = 1
        LIST = 2

    ValueTypeConvertFoo = {
        ValueType.INT: int,
        ValueType.FLOAT: float,
        ValueType.LIST: lambda s: [float(val) for val in s.split(',')]
    }

    MEASURE_SECTION = "Measure"
    FIXED_STEP_KEY = "fixed_step_list"
    FIXED_STEP_DEFAULT = "0.0001,0.01,0.1,1,10,20,100"

    FIXED_STEP_IDX_KEY = "fixed_step_idx"
    FIXED_STEP_IDX_DEFAULT = "0"

    STEP_ROUGH_KEY = "rough_step"
    STEP_ROUGH_DEFAULT = "0.5"

    STEP_COMMON_KEY = "common_step"
    STEP_COMMON_DEFAULT = "0.05"

    STEP_EXACT_KEY = "exact_step"
    STEP_EXACT_DEFAULT = "0.002"

    START_DEVIATION_KEY = "start_deviation"
    START_DEVIATION_DEFAULT = "5"

    fixed_step_changed = pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.__fixed_step_list = []
        self.__fixed_step_idx = 0

        self.__rough_step = 0
        self.__common_step = 0
        self.__exact_step = 0
        self.__start_deviation = 0

        self.settings = configparser.ConfigParser()
        try:
            self.restore_settings()
        except configparser.ParsingError:
            raise BadIniException

    # noinspection DuplicatedCode
    def restore_settings(self):
        if not os.path.exists(self.CONFIG_PATH):
            self.settings[self.MEASURE_SECTION] = {self.FIXED_STEP_KEY: self.FIXED_STEP_DEFAULT,
                                                   self.FIXED_STEP_IDX_KEY: self.FIXED_STEP_IDX_DEFAULT,
                                                   self.STEP_ROUGH_KEY: self.STEP_ROUGH_DEFAULT,
                                                   self.STEP_COMMON_KEY: self.STEP_COMMON_DEFAULT,
                                                   self.STEP_EXACT_KEY: self.STEP_EXACT_DEFAULT,
                                                   self.START_DEVIATION_KEY: self.START_DEVIATION_DEFAULT}
            utils.save_settings(self.CONFIG_PATH, self.settings)
        else:
            self.settings.read(self.CONFIG_PATH)
            self.add_ini_section(self.MEASURE_SECTION)

        self.__fixed_step_list = self.check_ini_value(self.MEASURE_SECTION, self.FIXED_STEP_KEY,
                                                      self.FIXED_STEP_DEFAULT, self.ValueType.LIST)

        self.__fixed_step_idx = self.check_ini_value(self.MEASURE_SECTION, self.FIXED_STEP_IDX_KEY,
                                                     self.FIXED_STEP_IDX_DEFAULT, self.ValueType.INT)
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)

        self.__rough_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_ROUGH_KEY,
                                                 self.STEP_ROUGH_DEFAULT, self.ValueType.FLOAT)
        self.__rough_step = utils.bound(self.__rough_step, 0., 100.)

        self.__common_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_COMMON_KEY,
                                                  self.STEP_COMMON_DEFAULT, self.ValueType.FLOAT)
        self.__common_step = utils.bound(self.__common_step, 0., 100.)

        self.__exact_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_EXACT_KEY,
                                                 self.STEP_EXACT_DEFAULT, self.ValueType.FLOAT)
        self.__exact_step = utils.bound(self.__exact_step, 0., 100.)

        self.__start_deviation = self.check_ini_value(self.MEASURE_SECTION, self.START_DEVIATION_KEY,
                                                      self.START_DEVIATION_DEFAULT, self.ValueType.INT)
        self.__start_deviation = utils.bound(self.__start_deviation, 0, 100)

        # Выводит ini файл в консоль
        # for key in settings:
        #     print(f"[{key}]")
        #     for subkey in settings[key]:
        #         print(f"{subkey} = {settings[key][subkey]}")

    def add_ini_section(self, a_name: str):
        if not self.settings.has_section(a_name):
            self.settings.add_section(a_name)

    def check_ini_value(self, a_section, a_key, a_default, a_value_type: ValueType):
        try:
            value = self.ValueTypeConvertFoo[a_value_type](self.settings[a_section][a_key])
        except (KeyError, ValueError):
            self.settings[a_section][a_key] = a_default
            utils.save_settings(self.CONFIG_PATH, self.settings)
            value = self.ValueTypeConvertFoo[a_value_type](a_default)
        return value

    def save(self):
        utils.save_settings(self.CONFIG_PATH, self.settings)

    @property
    def fixed_step_list(self):
        return self.__fixed_step_list

    @fixed_step_list.setter
    def fixed_step_list(self, a_list: List[float]):
        # Удаляет дубликаты
        final_list = list(dict.fromkeys(a_list))
        final_list.sort()

        saved_string = ','.join(str(val) for val in final_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.FIXED_STEP_KEY] = saved_string
        self.save()

        self.__fixed_step_list = [float(val) for val in final_list]
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)
        self.fixed_step_changed.emit()

    @property
    def fixed_step_idx(self):
        return self.__fixed_step_idx

    @fixed_step_idx.setter
    def fixed_step_idx(self, a_idx: int):
        self.settings[self.MEASURE_SECTION][self.FIXED_STEP_IDX_KEY] = str(a_idx)
        self.save()

        self.__fixed_step_idx = a_idx
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)

    @property
    def rough_step(self):
        return self.__rough_step

    @rough_step.setter
    def rough_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_ROUGH_KEY] = str(a_step)
        self.save()

        self.__rough_step = a_step
        self.__rough_step = utils.bound(self.__rough_step, 0., 100.)

    @property
    def common_step(self):
        return self.__common_step

    @common_step.setter
    def common_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_COMMON_KEY] = str(a_step)
        self.save()

        self.__common_step = a_step
        self.__common_step = utils.bound(self.__common_step, 0., 100.)

    @property
    def exact_step(self):
        return self.__exact_step

    @exact_step.setter
    def exact_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_EXACT_KEY] = str(a_step)
        self.save()

        self.__exact_step = a_step
        self.__exact_step = utils.bound(self.__exact_step, 0., 100.)

    @property
    def start_deviation(self):
        return self.__start_deviation

    @start_deviation.setter
    def start_deviation(self, a_step: int):
        self.settings[self.MEASURE_SECTION][self.START_DEVIATION_KEY] = str(a_step)
        self.save()

        self.__start_deviation = a_step
        self.__start_deviation = utils.bound(self.__start_deviation, 0, 100)


