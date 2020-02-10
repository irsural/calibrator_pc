from typing import List

import calibrator_constants as clb
from constants import DeviceSystem, Point, Mark
import utils


class TemplateParams:
    def __init__(self, a_name="Новый шаблон", a_organisation="", a_etalon_device="", a_device_name="",
                 a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC, a_signal_type=clb.SignalType.ACI,
                 a_device_class=0.05, a_points: List[Point] = None, a_marks: List[Mark] = None):
        self.name = a_name
        self.organisation = a_organisation
        self.etalon_device = a_etalon_device
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.signal_type = a_signal_type
        self.device_class = a_device_class
        self.points: List[Point] = a_points if a_points is not None else []
        self.marks: List[Mark] = a_marks if a_marks is not None else []


class TemplatesDB:
    def __init__(self, a_db_name="templates"):
        self.names = []

    def add(self, a_params: TemplateParams):
        if self.is_name_exist(a_params.name):
            return False
        else:
            self.names.append(a_params.name)
            return True

    def get(self, a_name: str):
        if a_name in self.names:
            return TemplateParams(a_name)
        else:
            return None

    def edit(self, a_name: str, a_params: TemplateParams):
        if self.is_name_exist(a_params.name) and (a_name != a_params.name):
            # Если имя изменилось и оно уже существует
            return False
        else:
            self.names.append(a_params.name)
            if a_name in self.names:
                self.names.remove(a_name)
            return True

    def delete(self, a_name: str):
        if a_name in self.names:
            self.names.remove(a_name)
            return True
        else:
            return False

    def is_name_exist(self, a_name: str):
        return a_name in self.names

