from typing import List
import sqlite3

import calibrator_constants as clb
from constants import DeviceSystem, Point, Mark
import utils


class TemplateParams:
    def __init__(self, a_name="Новый шаблон", a_organisation="", a_etalon_device="", a_device_name="",
                 a_device_creator="", a_device_system=DeviceSystem.MAGNETOELECTRIC, a_signal_type=clb.SignalType.ACI,
                 a_device_class=0.05, a_points: List[Point] = None):
        self.name = a_name
        self.organisation = a_organisation
        self.etalon_device = a_etalon_device
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.signal_type = a_signal_type
        self.device_class = a_device_class
        self.points: List[Point] = a_points if a_points is not None else []


class TemplatesDB:
    def __init__(self, a_db_name="templates.db"):
        self.connection = sqlite3.connect(a_db_name)
        self.cursor = self.connection.cursor()

        self.templates_tab = "templates"
        self.points_tab = "poitns"

        self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.templates_tab} "
                f"(id integer primary key autoincrement, name text, organisation text, etalon_device text," 
                f"device_name text, device_creator text, device_system integer, signal_type integer,"
                f"device_class real)"
            )

        self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.points_tab} "
                f"(id integer primary key autoincrement, amplitude real, frequency real, template_id int,"
                f"foreign key (template_id) references {self.templates_tab}(id))"
            )

    def __del__(self):
        self.connection.close()

    def add(self, a_params: TemplateParams):
        if self.is_name_exist(a_params.name):
            return False
        else:
            with self.connection:
                self.cursor.execute(
                    f"insert into {self.templates_tab}(name, organisation, etalon_device, device_name, device_creator,"
                    f"device_system, signal_type, device_class) VALUES(?,?,?,?,?,?,?,?)",
                    (a_params.name, a_params.organisation, a_params.etalon_device, a_params.device_name,
                     a_params.device_creator, a_params.device_system, a_params.signal_type, a_params.device_class)
                )
            return True

    def get(self, a_name: str):
        try:
            self.cursor.execute(f"select * from {self.templates_tab} WHERE name='{a_name}'")
            record = self.cursor.fetchall()[0]
            return self.__row_to_template_params(record)
        except Exception as err:
            print(err)

    @staticmethod
    def __row_to_template_params(self, a_row: list):
        return TemplateParams(a_name=a_row[1], a_organisation=a_row[2], a_etalon_device=a_row[3],
                              a_device_name=a_row[4], a_device_creator=a_row[5], a_device_system=a_row[6],
                              a_signal_type=a_row[7], a_device_class=a_row[8])

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
        with self.connection:
            self.cursor.execute(f"delete from {self.templates_tab} WHERE name = '{a_name}'")
            return True

    def is_name_exist(self, a_name: str):
        c = self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {self.templates_tab} WHERE name='{a_name}')")
        res = c.fetchone()
        return res[0]

    def __iter__(self):
        self.cursor.execute(f"select * from {self.templates_tab}")
        return self

    def __next__(self) -> TemplateParams:
        res = self.cursor.fetchone()
        if res is None:
            raise StopIteration
        else:
            return self.__row_to_template_params(res)
