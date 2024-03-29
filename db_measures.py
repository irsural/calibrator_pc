from collections import namedtuple
from enum import IntEnum
from typing import List
import sqlite3

from PyQt5.QtCore import QDate, QTime

from variable_template_fields_dialog import VariableTemplateParams
from new_fast_measure_dialog import FastMeasureParams
from db_templates import TemplateParams
from constants import DeviceSystem, enum_to_device_system
import irspy.clb.calibrator_constants as clb
from irspy import utils


class MeasureColumn(IntEnum):
    ID = 0
    DATETIME = 1
    DEVICE_NAME = 2
    DEVICE_CREATOR = 3
    DEVICE_SYSTEM = 4
    OWNER = 5
    USER = 6
    SERIAL_NUMBER = 7
    COMMENT = 8


MEASURE_COLUMN_TO_NAME = {
    MeasureColumn.ID: "Id",
    MeasureColumn.DATETIME: "Дата / Время",
    MeasureColumn.DEVICE_NAME: "Наименование\nприбора",
    MeasureColumn.DEVICE_CREATOR: "Изготовитель",
    MeasureColumn.DEVICE_SYSTEM: "Система",
    MeasureColumn.OWNER: "Организация\nвладелец",
    MeasureColumn.USER: "Поверитель",
    MeasureColumn.SERIAL_NUMBER: "Заводской\nномер",
    MeasureColumn.COMMENT: "Комментарий",
}

MeasuredPoint = namedtuple("Point", ["scale_point", "amplitude", "frequency", "up_value", "down_value"])


class Measure:
    class Case:
        def __init__(self, a_id=0, a_limit=1e-9, a_class=0.05, a_signal_type=clb.SignalType.ACI, a_minimal_discrete=0,
                     a_scale_coef=1, a_points: List[MeasuredPoint] = None):
            self.id = a_id
            self.limit = a_limit
            self.device_class = a_class
            self.signal_type = a_signal_type
            self.minimal_discrete = a_minimal_discrete
            self.scale_coef = a_scale_coef
            self.points = a_points if a_points is not None else []

    def __init__(self, a_cases: List[Case], a_id=0,  a_device_name="", a_device_creator="",
                 a_device_system=DeviceSystem.MAGNETOELECTRIC, a_user="", a_date="", a_serial_num="", a_owner="",
                 a_comment="", a_time=None):

        self.id = a_id

        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system

        self.owner = a_owner
        self.user = a_user
        self.serial_num = a_serial_num
        self.date = a_date if a_date else QDate.currentDate().toString("dd.MM.yyyy")
        self.time = QTime.currentTime().toString("H:mm:ss") if a_time is None else a_time

        self.comment = a_comment

        self.cases = a_cases

    @classmethod
    def from_fast_params(cls, a_params: FastMeasureParams):
        if a_params.frequency:
            frequency_list = (float(f) for f in a_params.frequency.split(';'))
        else:
            frequency_list = [0] if clb.is_dc_signal[a_params.signal_type] else [50]

        points = [MeasuredPoint(scale_point=0, amplitude=float(p),
                                frequency=clb.bound_frequency(float(f), a_params.signal_type),
                                up_value=0, down_value=0)
                  for f in frequency_list for p in a_params.amplitudes]
        measure_case = Measure.Case(a_id=0, a_limit=a_params.upper_bound, a_class=a_params.accuracy_class,
                                    a_signal_type=a_params.signal_type, a_minimal_discrete=a_params.minimal_discrete,
                                    a_scale_coef=0, a_points=points)

        return cls(a_comment=a_params.comment, a_cases=[measure_case])

    @classmethod
    def from_template(cls, a_params: TemplateParams, a_var_params: VariableTemplateParams):
        measure_cases = []
        for scale in a_params.scales:
            for limit in scale.limits:
                if limit.frequency:
                    frequency_list = (float(f) for f in limit.frequency.split(';'))
                else:
                    frequency_list = [0] if clb.is_dc_signal[limit.signal_type] else [50]

                if scale.points:
                    scale_coef = limit.limit / max(scale.points)
                    minimal_discrete = round(utils.get_array_min_diff(scale.points) * scale_coef, 9)

                    points = [MeasuredPoint(scale_point=p,
                                            amplitude=clb.bound_amplitude(p * scale_coef, limit.signal_type),
                                            frequency=clb.bound_frequency(float(f), limit.signal_type),
                                            up_value=0, down_value=0)
                              for f in frequency_list for p in scale.points]
                else:
                    scale_coef = 1
                    minimal_discrete = 1
                    points = []

                measure_cases.append(Measure.Case(a_id=0, a_limit=limit.limit, a_class=limit.device_class,
                                                  a_signal_type=limit.signal_type, a_minimal_discrete=minimal_discrete,
                                                  a_scale_coef=scale_coef, a_points=points))

        return cls(measure_cases, a_device_name=a_params.device_name, a_device_creator=a_params.device_creator,
                   a_device_system=a_params.device_system, a_user=a_var_params.user_name, a_date=a_var_params.date,
                   a_serial_num=a_var_params.serial_num, a_owner=a_var_params.owner)


class MeasuresDB:
    def __init__(self, a_db_connection: sqlite3.Connection):
        self.connection = a_db_connection
        self.cursor = self.connection.cursor()

    @staticmethod
    def create_db(a_db_name: str):
        connection = sqlite3.connect(a_db_name)
        cursor = connection.cursor()
        with connection:
            cursor.execute("CREATE TABLE IF NOT EXISTS measures "
                           "(id integer primary key autoincrement, datetime text, device_name text, "
                           "device_creator text, device_system integer, owner text, user text, "
                           "serial_number text, comment text)")

            cursor.execute("CREATE TABLE IF NOT EXISTS measure_cases "
                           "(id integer primary key autoincrement, measure_limit real, device_class real, "
                           "signal_type int, measure_id int, "
                           "foreign key (measure_id) references measures(id))")

            cursor.execute("CREATE TABLE IF NOT EXISTS results "
                           "(id integer primary key autoincrement, scale_point real, amplitude real, frequency real, "
                           "up_value real, down_value real, measure_case_id int,"
                           "foreign key (measure_case_id) references measure_cases(id))")

            cursor.execute("CREATE TABLE IF NOT EXISTS marks "
                           "(name text primary key, tag text unique, default_value text)")

            cursor.execute("CREATE TABLE IF NOT EXISTS mark_values "
                           "(id integer primary key autoincrement, value text, mark_name text,  measure_id int, "
                           "unique (mark_name, measure_id), "
                           "foreign key (mark_name) references marks (name),"
                           "foreign key (measure_id) references measures(id))")

            # Таблицы соответствий системы прибора и типа сигнала
            cursor.execute("CREATE TABLE IF NOT EXISTS system (id integer primary key, name text unique)")
            systems_table = [(system, enum_to_device_system[system]) for system in DeviceSystem]
            cursor.executemany("insert or ignore into system (id, name) values (?, ?)", systems_table)

            cursor.execute("CREATE TABLE IF NOT EXISTS signal_type (id integer primary key, name text unique)")
            signal_types = [(signal_type, clb.signal_type_to_text_short[signal_type]) for signal_type in clb.SignalType]
            cursor.executemany("insert or ignore into signal_type (id, name) values (?, ?)", signal_types)

        return connection

    def new_measure(self, a_measure: Measure):
        with self.connection:
            self.cursor.execute("insert into measures (datetime, device_name, device_creator, device_system, owner, "
                                "user, serial_number, comment) values (?, ?, ?, ?, ?, ?, ?, ?)",
                                (' '.join([a_measure.date, a_measure.time]), a_measure.device_name,
                                 a_measure.device_creator, a_measure.device_system, a_measure.owner, a_measure.user,
                                 a_measure.serial_num, a_measure.comment))
            measure_id = self.cursor.lastrowid
            # Копируем все дефолтные значения в измерение, если дефолтное значение заполнено
            self.cursor.execute("insert into mark_values (mark_name, value, measure_id) "
                                "select name, default_value, {0} from marks  "
                                "where default_value != ''".format(measure_id))
        return measure_id

    def update_measure(self, a_measure: Measure):
        assert self.is_measure_exist(a_measure.id), "Row for updated measure must exist!"

        with self.connection:
            self.cursor.execute(
                "update measures set datetime = ?, device_name = ?, device_creator = ?, device_system = ?, "
                "owner = ?, user = ?, serial_number = ?, comment = ? where id = {0}".format(a_measure.id),
                (' '.join([a_measure.date, a_measure.time]), a_measure.device_name, a_measure.device_creator,
                 a_measure.device_system, a_measure.owner, a_measure.user, a_measure.serial_num, a_measure.comment)
            )

    def new_case(self, a_measure_id, a_case: Measure.Case):
        with self.connection:
            self.cursor.execute("insert into measure_cases (measure_limit, device_class, signal_type, measure_id) "
                                "values (?, ?, ?, ?)",
                                (a_case.limit, a_case.device_class, a_case.signal_type, a_measure_id))
            case_id = self.cursor.lastrowid
        return case_id

    def update_case(self, a_case: Measure.Case):
        assert a_case.id != 0, "Case id must not be zero!!!"
        with self.connection:
            self.cursor.execute("update measure_cases set measure_limit = ?, device_class = ?, signal_type = ? "
                                "where id = {0}".format(a_case.id),
                                (a_case.limit, a_case.device_class, a_case.signal_type))

    # def delete_case(self, a_case_id: int):
    #     assert a_case_id != 0, "Case id must not be zero!!!"
    #     with self.connection:
    #         self.cursor.execute(f"delete from measure_cases where id = {a_case_id}")
    #         self.cursor.execute(f"delete from results where measure_case_id = {a_case_id}")

    def save_points(self, a_measure: Measure):
        assert a_measure.id != 0, "Measure id must not be zero"
        with self.connection:
            self.cursor.executemany("insert into results (scale_point, amplitude, frequency, up_value, down_value, "
                                    "measure_case_id) values (?, ?, ?, ?, ?, ?)",
                                    ((point.scale_point, point.amplitude, point.frequency, point.up_value,
                                      point.down_value, case.id)
                                     for case in a_measure.cases for point in case.points))

    def save_measure(self, a_measure: Measure):
        self.update_measure(a_measure)
        for case in a_measure.cases:
            case.id = self.new_case(a_measure.id, case)
        self.save_points(a_measure)

    def get(self, a_id: int) -> Measure:
        self.cursor.execute("select * from measures where id={0}".format(a_id))
        measure_data = self.cursor.fetchone()
        date, time = measure_data[MeasureColumn.DATETIME].split(' ')

        measure = Measure(a_cases=[], a_id=measure_data[MeasureColumn.ID], a_date=date,
                          a_device_name=measure_data[MeasureColumn.DEVICE_NAME],
                          a_device_creator=measure_data[MeasureColumn.DEVICE_CREATOR],
                          a_device_system=measure_data[MeasureColumn.DEVICE_SYSTEM],
                          a_owner=measure_data[MeasureColumn.OWNER],
                          a_user=measure_data[MeasureColumn.USER],
                          a_serial_num=measure_data[MeasureColumn.SERIAL_NUMBER],
                          a_comment=measure_data[MeasureColumn.COMMENT],
                          a_time=time
                          )

        self.cursor.execute("select * from measure_cases where measure_id = {0}".format(measure.id))
        case_data = self.cursor.fetchall()

        for case_row in case_data:
            case_id = case_row[0]

            self.cursor.execute("select scale_point, amplitude, frequency, up_value, down_value from results "
                                "where measure_case_id={0}".format(case_id))
            points = [MeasuredPoint(*point_data) for point_data in self.cursor.fetchall()]

            measure.cases.append(Measure.Case(a_id=case_id, a_limit=case_row[1], a_class=case_row[2],
                                              a_signal_type=case_row[3], a_points=points))

        return measure

    def delete(self, a_measure_id: int):
        assert self.is_measure_exist(a_measure_id), "deleted id must exist!"
        with self.connection:
            self.cursor.execute("delete from mark_values where measure_id={0}".format(a_measure_id))

            self.cursor.execute("delete from results where measure_case_id in "
                                "(select id from measure_cases where "
                                "measure_cases.measure_id={0})".format(a_measure_id))

            self.cursor.execute("delete from measure_cases where measure_id={0}".format(a_measure_id))
            self.cursor.execute("delete from measures where id={0}".format(a_measure_id))

    def is_measure_exist(self, a_id: int):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM measures WHERE id='{0}')".format(a_id))
        res = self.cursor.fetchone()
        return res[0]
