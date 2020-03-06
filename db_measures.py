from collections import namedtuple
from typing import List, Tuple
from enum import IntEnum
import sqlite3

from PyQt5.QtCore import QDate, QTime

from variable_template_fields_dialog import VariableTemplateParams
from new_fast_measure_dialog import FastMeasureParams
from db_templates import TemplateParams
from constants import DeviceSystem, MeasuredPoint, Scale, enum_to_device_system
import calibrator_constants as clb



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
    def __init__(self, a_scales: Scale, a_id=0,  a_device_name="", a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC,
                 a_user="", a_date="", a_serial_num="", a_owner="", a_comment="", a_minimal_discrete=0.):

        self.id = a_id

        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system

        self.owner = a_owner
        self.user = a_user
        self.serial_num = a_serial_num
        self.date = a_date if a_date else QDate.currentDate().toString("dd.MM.yyyy")

        self.comment = a_comment
        self.minimal_discrete = a_minimal_discrete

        self.time = QTime.currentTime().toString("H:mm:ss")

        # if a_upper_bound is not None:
        #     self.upper_bound = a_upper_bound
        # elif a_points:
        #     self.upper_bound = max(a_points, key=lambda p: p.amplitude).amplitude
        # else:
        #     self.upper_bound = 0
        #
        # self.upper_bound = clb.bound_amplitude(self.upper_bound, self.signal_type)
        # self.lower_bound = -self.upper_bound if a_lower_bound is None else \
        #     clb.bound_amplitude(a_lower_bound, self.signal_type)

    @classmethod
    def fromFastParams(cls, a_params: FastMeasureParams):
        points = [MeasuredPoint(amplitude=float(p), frequency=clb.bound_frequency(float(f), a_params.signal_type),
                                up_value=0, down_value=0) for f in a_params.frequency for p in a_params.amplitudes]
        scales = None

        return cls(a_scales=scales, a_minimal_discrete=a_params.minimal_discrete, a_comment=a_params.comment,
                   a_upper_bound=a_params.upper_bound)

    @classmethod
    def fromTemplate(cls, a_params: TemplateParams, a_var_params: VariableTemplateParams):
        scales = None

        return cls(a_scales=scales, a_device_name=a_params.device_name, a_device_creator=a_params.device_creator,
                   a_device_system=a_params.device_system, a_user=a_var_params.user_name, a_date=a_var_params.date,
                   a_serial_num=a_var_params.serial_num, a_owner=a_var_params.owner)


class MeasuresDB:
    def __init__(self, a_db_connection: sqlite3.Connection):
        self.connection = a_db_connection
        self.cursor = self.connection.cursor()

    def create(self):
        with self.connection:
            self.cursor.execute(f"insert into measures default values")
            measure_id = self.cursor.lastrowid
            # Копируем все дефолтные значения в измерение, если дефолтное значение заполнено
            self.cursor.execute(f"insert into mark_values (mark_name, value, measure_id) "
                                f"select name, default_value, {measure_id} from marks  "
                                f"where default_value != ''")
        return measure_id

    @staticmethod
    def create_db(a_db_name: str):
        connection = sqlite3.connect(a_db_name)
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS marks "
                           f"(name text primary key, tag text unique, default_value text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS measures "
                           f"(id integer primary key autoincrement, datetime text, device_name text, "
                           f"serial_number text, comment text, owner text, device_system integer, "
                           f"user text, device_creator text)")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS mark_values "
                           f"(id integer primary key autoincrement, value text, mark_name text,  measure_id int, "
                           f"unique (mark_name, measure_id), "
                           f"foreign key (mark_name) references marks (name),"
                           f"foreign key (measure_id) references measures(id))")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS results "
                           f"(id integer primary key autoincrement, point real, frequency real, up_value real, "
                           f"down_value real, measure_id int,"
                           f"foreign key (measure_id) references measures(id))")

            # Таблицы соответствий системы прибора и типа сигнала
            cursor.execute(f"CREATE TABLE IF NOT EXISTS system (id integer primary key, name text unique)")
            systems_table = [(system, enum_to_device_system[system]) for system in DeviceSystem]
            cursor.executemany(f"insert or ignore into system (id, name) values (?, ?)", systems_table)

            cursor.execute(f"CREATE TABLE IF NOT EXISTS signal_type (id integer primary key, name text unique)")
            signal_types = [(signal_type, clb.enum_to_signal_type_short[signal_type]) for signal_type in clb.SignalType]
            cursor.executemany(f"insert or ignore into signal_type (id, name) values (?, ?)", signal_types)

        return connection

    def get(self, a_id: int) -> MeasureParams:
        self.cursor.execute(f"select point, frequency, up_value, down_value from results where measure_id={a_id}")
        points: list = self.cursor.fetchall()

        self.cursor.execute(f"select * from measures where id={a_id}")
        measure_data = self.cursor.fetchone()
        date, time = measure_data[MeasureColumn.DATETIME].split(' ')

        return MeasureParams(a_id=measure_data[MeasureColumn.ID],
                             a_date=date,
                             a_device_name=measure_data[MeasureColumn.DEVICE_NAME],
                             a_serial_num=measure_data[MeasureColumn.SERIAL_NUMBER],
                             a_comment=measure_data[MeasureColumn.COMMENT],
                             a_owner=measure_data[MeasureColumn.OWNER],
                             a_device_system=measure_data[MeasureColumn.DEVICE_SYSTEM],
                             a_user=measure_data[MeasureColumn.USER],
                             a_device_creator=measure_data[MeasureColumn.DEVICE_CREATOR]
                             )

    def save(self, a_params: MeasureParams, a_save_points: bool):
        assert self.is_measure_exist(a_params.id), "Row for saved measure must exist!"
        with self.connection:
            self.cursor.execute(
                f"update measures set device_name = ?, device_creator = ?, device_system = ?, "
                f"serial_number = ?, comment = ?, owner = ?, user = ?, datetime = ? where id = {a_params.id}",
                (a_params.device_name, a_params.device_creator, a_params.device_system, a_params.serial_num,
                 a_params.comment, a_params.owner, a_params.user, ' '.join([a_params.date, a_params.time]))
            )

            if a_save_points:
                self.cursor.executemany(f"insert into results (point, frequency, up_value, down_value, "
                                        f"measure_id) values (?, ?, ?, ?, {a_params.id})", a_params.points)

    def delete(self, a_id: int):
        assert self.is_measure_exist(a_id), "deleted id must exist!"
        with self.connection:
            self.cursor.execute(f"delete from mark_values where measure_id={a_id}")
            self.cursor.execute(f"delete from results where measure_id={a_id}")
            self.cursor.execute(f"delete from measures where id={a_id}")

    def is_measure_exist(self, a_id: int):
        self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM measures WHERE id='{a_id}')")
        res = self.cursor.fetchone()
        return res[0]
