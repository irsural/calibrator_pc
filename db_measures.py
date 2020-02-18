from collections import namedtuple
from typing import List
import sqlite3

from variable_template_fields_dialog import VariableTemplateParams
from new_fast_measure_dialog import FastMeasureParams
from QNoTemplateMeasureModel import PointData
from constants import DeviceSystem
from db_templates import TemplateParams
import calibrator_constants as clb


MeasureTables = namedtuple("MeasureDB", ["marks_table", "mark_values_table", "measures_table", "results_table"])


class MeasureParams:
    def __init__(self, a_id=0, a_organisation="", a_etalon_device="", a_device_name="",
                 a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC, a_signal_type=clb.SignalType.ACI,
                 a_device_class=0.05, a_owner="", a_user="", a_serial_num="", a_date="", a_time="", a_comment="",
                 a_minimal_discrete=0., a_upper_bound=None, a_lower_bound=None, a_points: List[PointData] = None):
        self.id = a_id
        self.organisation = a_organisation
        self.etalon_device = a_etalon_device
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.signal_type = a_signal_type
        self.device_class = a_device_class

        self.owner = a_owner
        self.user = a_user
        self.serial_num = a_serial_num
        self.date = a_date
        self.time = a_time

        self.points: List[PointData] = a_points if a_points is not None else []

        self.comment = a_comment
        self.minimal_discrete = a_minimal_discrete

        if a_upper_bound is not None:
            self.upper_bound = a_upper_bound
        elif a_points:
            self.upper_bound = max(a_points, key=lambda p: p.point).point
        else:
            self.a_upper_bound = 0

        self.a_upper_bound = clb.bound_amplitude(self.upper_bound, self.signal_type)
        self.lower_bound = -self.a_upper_bound if a_lower_bound is None else \
            clb.bound_amplitude(a_lower_bound, self.signal_type)

    @classmethod
    def fromFastParams(cls, a_params: FastMeasureParams):
        points = [PointData(a_point=float(p), a_frequency=float(f)) for f in a_params.frequency
                                                                    for p in a_params.amplitudes]

        return cls(a_etalon_device="Калибратор N4-25", a_signal_type=a_params.signal_type,
                   a_minimal_discrete=a_params.minimal_discrete, a_device_class=a_params.accuracy_class,
                   a_date=a_params.date, a_time=a_params.time, a_comment=a_params.comment,
                   a_upper_bound=a_params.upper_bound, a_points=points)

    @classmethod
    def fromTemplate(cls, a_params: TemplateParams, a_var_params: VariableTemplateParams):
        points = [PointData(a_point=float(p), a_frequency=float(f)) for p, f in a_params.points]

        return cls(a_organisation=a_params.organisation, a_etalon_device=a_params.etalon_device,
                   a_device_name=a_params.device_name, a_device_creator=a_params.device_creator,
                   a_device_system=a_params.device_system, a_signal_type=a_params.signal_type,
                   a_device_class=a_params.device_class, a_points=points, a_owner=a_var_params.owner, 
                   a_user=a_var_params.user_name, a_date=a_var_params.date, a_time=a_var_params.time,
                   a_serial_num=a_var_params.serial_num)


class MeasuresDB:
    def __init__(self, a_db_connection: sqlite3.Connection, a_db_tables: MeasureTables):
        self.connection = a_db_connection
        self.cursor = self.connection.cursor()

        self.measure_table = a_db_tables.measures_table
        self.marks_table = a_db_tables.marks_table
        self.mark_values_table = a_db_tables.mark_values_table

    def create(self):
        with self.connection:
            self.cursor.execute(f"insert into {self.measure_table} default values")
            measure_id = self.cursor.lastrowid
            # Копируем все дефолтные значения в измерение, если дефолтное значение заполнено
            self.cursor.execute(f"insert into {self.mark_values_table} (mark_name, value, measure_id) "
                                f"select name, default_value, {measure_id} from {self.marks_table}  "
                                f"where default_value != ''")
        return measure_id

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
