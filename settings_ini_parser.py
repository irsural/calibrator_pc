import configparser
import os
from typing import List

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

import utils


class Settings(QtCore.QObject):
    CONFIG_PATH = "./settings.ini"

    MEASURE_SECTION = "Measure"
    FIXED_STEP_KEY = "fixed_step_list"
    FIXED_STEP_DEFAULT = "0.0001,0.01,0.1,1,10,20,100"

    FIXED_STEP_IDX_KEY = "fixed_step_idx"
    FIXED_STEP_IDX_DEFAULT = "0"

    fixed_step_changed = pyqtSignal()
    fixed_step_idx_changed = pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.__fixed_step_list = []
        self.__fixed_step_idx = 0

        self.settings = self.restore_settings(self.CONFIG_PATH)

    def restore_settings(self, a_path: str):
        settings = configparser.ConfigParser()

        if not os.path.exists(a_path):
            settings[self.MEASURE_SECTION] = {self.FIXED_STEP_KEY: self.FIXED_STEP_DEFAULT,
                                              self.FIXED_STEP_IDX_KEY: self.FIXED_STEP_IDX_DEFAULT}
            utils.save_settings(a_path, settings)
        else:
            settings.read(a_path)

        try:
            self.__fixed_step_list = settings[self.MEASURE_SECTION][self.FIXED_STEP_KEY].split(',')
        except KeyError:
            settings[self.MEASURE_SECTION][self.FIXED_STEP_KEY] = self.FIXED_STEP_DEFAULT
            utils.save_settings(a_path, settings)
            self.__fixed_step_list = self.FIXED_STEP_DEFAULT

        try:
            self.__fixed_step_idx = int(settings[self.MEASURE_SECTION][self.FIXED_STEP_IDX_KEY])
            self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)
        except ValueError:
            self.__fixed_step_idx = 0
        except KeyError:
            settings[self.MEASURE_SECTION][self.FIXED_STEP_IDX_KEY] = self.FIXED_STEP_IDX_DEFAULT
            utils.save_settings(a_path, settings)
            self.__fixed_step_idx = self.FIXED_STEP_IDX_DEFAULT




        # Выводит ini файл в консоль
        # for key in settings:
        #     print(f"[{key}]")
        #     for subkey in settings[key]:
        #         print(f"{subkey} = {settings[key][subkey]}")

        return settings

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

        saved_string = ','.join(utils.float_to_string(val) for val in final_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.FIXED_STEP_KEY] = saved_string
        self.save()

        self.__fixed_step_list = final_list
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
        self.fixed_step_idx_changed.emit()
