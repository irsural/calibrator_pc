from typing import List

from QNoTemplateMeasureModel import PointData
from new_no_template_measure_dialog import FastMeasureParams
from db_templates import TemplateParams
from variable_template_fields_dialog import VariableTemplateParams
from constants import DeviceSystem, Mark
import calibrator_constants as clb
import utils


class MeasureParams:
    def __init__(self, a_organisation="", a_etalon_device="", a_device_name="",
                 a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC, a_signal_type=clb.SignalType.ACI,
                 a_device_class=0.05, a_owner="", a_user="", a_date="", a_temperature="", a_wet="", a_pressure="",
                 a_warming_time="", a_points: List[PointData] = None, a_marks: List[Mark] = None):

        # self.id = a_id

        self.organisation = a_organisation
        self.etalon_device = a_etalon_device
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.signal_type = a_signal_type
        self.device_class = a_device_class

        self.owner = a_owner
        self.user = a_user
        self.date = a_date
        self.temperature = a_temperature
        self.wet = a_wet
        self.pressure = a_pressure
        self.warming_time = a_warming_time

        self.points: List[PointData] = a_points if a_points is not None else []
        self.marks: List[Mark] = a_marks if a_marks is not None else []

    @classmethod
    def fromFastParams(cls, a_params: FastMeasureParams):
        return cls()

    @classmethod
    def fromTemplate(cls, a_params: TemplateParams, a_var_params: VariableTemplateParams):
        points = [PointData(a_point=float(p), a_frequency=float(f)) for p, f in a_params.points]

        return cls(a_organisation=a_params.organisation, a_etalon_device=a_params.etalon_device,
                   a_device_name=a_params.device_name, a_device_creator=a_params.device_creator,
                   a_device_system=a_params.device_system, a_signal_type=a_params.signal_type,
                   a_device_class=a_params.device_class, a_points=points, a_owner=a_var_params.owner, 
                   a_user=a_var_params.user_name, a_date=a_var_params.date, a_temperature=a_var_params.temperature, 
                   a_wet=a_var_params.wet, a_pressure=a_var_params.pressure, a_warming_time=a_var_params.warming_time)


class MeasuresDB:
    def __init__(self, a_db_name="measures"):
        self.ids = []

    def add(self, a_params: MeasureParams):
        # self.ids.append(a_params.id)
        pass

    def get(self, a_id: str):
        if a_id in self.ids:
            return MeasureParams(a_id)
        else:
            return None

    def edit(self, a_id: str, a_params: MeasureParams):
        pass
        # if self.is_measure_exist(a_params.id) and (a_id != a_params.id):
        #     Если имя изменилось и оно уже существует
        #     return False
        # else:
        #     self.ids.append(a_params.id)
        #     if a_id in self.ids:
        #         self.ids.remove(a_id)
        #     return True

    def delete(self, a_id: str):
        if a_id in self.ids:
            self.ids.remove(a_id)
            return True
        else:
            return False

    def is_measure_exist(self, a_id: str):
        return a_id in self.ids

