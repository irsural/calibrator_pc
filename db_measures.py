from collections import namedtuple
from typing import List, Tuple
from enum import IntEnum
import sqlite3

from variable_template_fields_dialog import VariableTemplateParams
from new_fast_measure_dialog import FastMeasureParams
from db_templates import TemplateParams
from constants import DeviceSystem
import calibrator_constants as clb
from constants import Point

MeasureTables = namedtuple("MeasureDB", ["marks_table", "mark_values_table", "measures_table", "results_table",
                                         "system_table", "signal_type_table"])


class MeasureColumn(IntEnum):
    ID = 0
    DATETIME = 1
    DEVICE_NAME = 2
    SERIAL_NUMBER = 3
    SIGNAL_TYPE = 4
    DEVICE_CLASS = 5
    COMMENT = 6
    OWNER = 7
    DEVICE_SYSTEM = 8
    USER = 9
    ORGANISATION = 10
    ETALON_DEVICE = 11
    DEVICE_CREATOR = 12


MEASURE_COLUMN_TO_NAME = {
    MeasureColumn.ID: "Id",
    MeasureColumn.DATETIME: "Дата / Время",
    MeasureColumn.DEVICE_NAME: "Наименование\nприбора",
    MeasureColumn.SERIAL_NUMBER: "Заводской\nномер",
    MeasureColumn.SIGNAL_TYPE: "Род\nтока",
    MeasureColumn.DEVICE_CLASS: "Класс",
    MeasureColumn.COMMENT: "Комментарий",
    MeasureColumn.OWNER: "Организация\nвладелец",
    MeasureColumn.DEVICE_SYSTEM: "Система",
    MeasureColumn.USER: "Поверитель",
    MeasureColumn.ORGANISATION: "Организация\nповеритель",
    MeasureColumn.ETALON_DEVICE: "Средство\nповерки",
    MeasureColumn.DEVICE_CREATOR: "Изготовитель"
}


class MeasureParams:
    def __init__(self, a_id=0, a_organisation="", a_etalon_device="", a_device_name="",
                 a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC, a_signal_type=clb.SignalType.ACI,
                 a_device_class=0.05, a_owner="", a_user="", a_serial_num="", a_date="", a_time="", a_comment="",
                 a_minimal_discrete=0., a_upper_bound=None, a_lower_bound=None, a_points: List[Point] = None):
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

        self.points: List[Point] = a_points if a_points is not None else []

        self.comment = a_comment
        self.minimal_discrete = a_minimal_discrete

        if a_upper_bound is not None:
            self.upper_bound = a_upper_bound
        elif a_points:
            self.upper_bound = max(a_points, key=lambda p: p.amplitude).amplitude
        else:
            self.upper_bound = 0

        self.upper_bound = clb.bound_amplitude(self.upper_bound, self.signal_type)
        self.lower_bound = -self.upper_bound if a_lower_bound is None else \
            clb.bound_amplitude(a_lower_bound, self.signal_type)

    @classmethod
    def fromFastParams(cls, a_params: FastMeasureParams):
        points = [Point(amplitude=float(p), frequency=float(f))
                  for f in a_params.frequency for p in a_params.amplitudes]

        return cls(a_etalon_device="Калибратор N4-25", a_signal_type=a_params.signal_type,
                   a_minimal_discrete=a_params.minimal_discrete, a_device_class=a_params.accuracy_class,
                   a_date=a_params.date, a_time=a_params.time, a_comment=a_params.comment,
                   a_upper_bound=a_params.upper_bound, a_points=points)

    @classmethod
    def fromTemplate(cls, a_params: TemplateParams, a_var_params: VariableTemplateParams):
        points = [Point(amplitude=float(p), frequency=float(f)) for p, f in a_params.points]

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
        self.results_table = a_db_tables.results_table

    def create(self):
        with self.connection:
            self.cursor.execute(f"insert into {self.measure_table} default values")
            measure_id = self.cursor.lastrowid
            # Копируем все дефолтные значения в измерение, если дефолтное значение заполнено
            self.cursor.execute(f"insert into {self.mark_values_table} (mark_name, value, measure_id) "
                                f"select name, default_value, {measure_id} from {self.marks_table}  "
                                f"where default_value != ''")
        return measure_id

    def get(self, a_id: int):
        self.cursor.execute(f"select * from {self.results_table} where measure_id={a_id}")
        points: list = self.cursor.fetchall()

        self.cursor.execute(f"select * from {self.measure_table} where id={a_id}")
        measure_data = self.cursor.fetchone()
        date, time = measure_data[MeasureColumn.DATETIME].split(' ')

        return MeasureParams(a_id=measure_data[MeasureColumn.ID],
                             a_date=date,
                             a_time=time,
                             a_device_name=measure_data[MeasureColumn.DEVICE_NAME],
                             a_serial_num=measure_data[MeasureColumn.SERIAL_NUMBER],
                             a_signal_type=measure_data[MeasureColumn.SIGNAL_TYPE],
                             a_device_class=measure_data[MeasureColumn.DEVICE_CLASS],
                             a_comment=measure_data[MeasureColumn.COMMENT],
                             a_owner=measure_data[MeasureColumn.OWNER],
                             a_device_system=measure_data[MeasureColumn.DEVICE_SYSTEM],
                             a_user=measure_data[MeasureColumn.USER],
                             a_organisation=measure_data[MeasureColumn.ORGANISATION],
                             a_etalon_device=measure_data[MeasureColumn.ETALON_DEVICE],
                             a_device_creator=measure_data[MeasureColumn.DEVICE_CREATOR]), points

    def save(self, a_params: MeasureParams, points_data: Tuple[List]):
        assert self.is_measure_exist(a_params.id), "Row for saved measure must exist!"
        with self.connection:
            self.cursor.execute(f"update {self.measure_table} set organisation = ?, etalon_device = ?,"
                                f"device_name = ?, device_creator = ?, device_system = ?, signal_type = ?,"
                                f"device_class = ?, serial_number = ?, comment = ?, owner = ?, user = ?, datetime = ? "
                                f"where id = {a_params.id}",
                                (a_params.organisation, a_params.etalon_device, a_params.device_name,
                                 a_params.device_creator, a_params.device_system, a_params.signal_type,
                                 a_params.device_class, a_params.serial_num, a_params.comment, a_params.owner,
                                 a_params.user, ' '.join([a_params.date, a_params.time])))

            self.cursor.executemany(f"insert into {self.results_table} (point, frequency, up_value, down_value, "
                                    f"measure_id) values (?, ?, ?, ?, {a_params.id})", points_data)

    def delete(self, a_id: int):
        assert self.is_measure_exist(a_id), "deleted id must exist!"
        with self.connection:
            self.cursor.execute(f"delete from {self.mark_values_table} where measure_id={a_id}")
            self.cursor.execute(f"delete from {self.results_table} where measure_id={a_id}")
            self.cursor.execute(f"delete from {self.measure_table} where id={a_id}")

    def is_measure_exist(self, a_id: int):
        self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {self.measure_table} WHERE id='{a_id}')")
        res = self.cursor.fetchone()
        return res[0]
