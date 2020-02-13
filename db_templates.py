from typing import List
import sqlite3

import calibrator_constants as clb
from constants import DeviceSystem, Point


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
                template_id = self.cursor.lastrowid
                self.__add_points(a_params.points, template_id)
            return True

    def get(self, a_name: str):
        try:
            self.cursor.execute(f"select * from {self.templates_tab} WHERE name='{a_name}'")
            record = self.cursor.fetchone()

            template_id = record[0]
            self.cursor.execute(f"select amplitude, frequency from {self.points_tab} where template_id={template_id}")
            points = self.cursor.fetchall()

            return self.__row_to_template_params(record, points)
        except Exception as err:
            print(err)

    @staticmethod
    def __row_to_template_params(a_row: list, a_points: tuple):
        return TemplateParams(a_name=a_row[1], a_organisation=a_row[2], a_etalon_device=a_row[3],
                              a_device_name=a_row[4], a_device_creator=a_row[5], a_device_system=a_row[6],
                              a_signal_type=a_row[7], a_device_class=a_row[8],
                              a_points=[Point(amplitude=a, frequency=f) for a, f in a_points])

    def __add_points(self, a_points: list, a_template_id):
        points = ((a, f) for (a, f) in a_points)
        self.cursor.executemany(f"insert into {self.points_tab} (amplitude, frequency, template_id) "
                                f"values (?,?,{a_template_id})", points)

    def edit(self, a_name: str, a_params: TemplateParams, a_rewrite_points: bool):
        if self.is_name_exist(a_params.name) and (a_name != a_params.name):
            # Если имя изменилось и оно уже существует
            return False
        else:
            with self.connection:
                self.cursor.execute(
                    f"update {self.templates_tab} set name = ?, organisation = ?, etalon_device = ?, device_name = ?, "
                    f"device_creator = ?, device_system = ?, signal_type = ?, device_class = ? "
                    f"where name = '{a_name}'",
                    (a_params.name, a_params.organisation, a_params.etalon_device, a_params.device_name,
                     a_params.device_creator, a_params.device_system, a_params.signal_type, a_params.device_class)
                )

                if a_rewrite_points:
                    self.cursor.execute(f"select id from {self.templates_tab} where name = '{a_params.name}'")
                    template_id = self.cursor.fetchone()[0]

                    self.cursor.execute(f"delete from {self.points_tab} where template_id={template_id}")
                    self.__add_points(a_params.points, template_id)
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
        # Итерация по именам БД
        self.cursor.execute(f"select name from {self.templates_tab} order by id")
        return self

    def __next__(self) -> TemplateParams:
        res = self.cursor.fetchone()
        if res is None:
            raise StopIteration
        else:
            return res[0]
