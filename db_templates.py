from typing import List
import sqlite3

import calibrator_constants as clb
from constants import DeviceSystem, MeasuredPoint, Scale


class TemplateParams:
    def __init__(self, a_id=0, a_name="Новый шаблон", a_device_name="", a_device_creator="",
                 a_device_system=DeviceSystem.MAGNETOELECTRIC, a_scales: List[Scale] = None):
        self.id = a_id
        self.name = a_name
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.scales = a_scales if a_scales else []


class TemplatesDB:
    def __init__(self, a_db_name="templates.db"):
        self.connection = sqlite3.connect(a_db_name)
        self.cursor = self.connection.cursor()

        self.templates_tab = "templates"
        self.scales_tab = "scales"
        self.limits_tab = "limits"

        with self.connection:
            self.cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.templates_tab} "
                    f"(id integer primary key autoincrement, name text, device_name text, device_creator text, "
                    f"device_system integer)"
                )

            self.cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.scales_tab} "
                    f"(id integer primary key autoincrement, scale_number int, point real, template_id int,"
                    f"foreign key (template_id) references {self.templates_tab}(id))"
                )

            self.cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.limits_tab} "
                    f"(id integer primary key autoincrement, scale_limit real, signal_type int, device_class real, "
                    f"frequency text, scale_id int, "
                    f"foreign key (scale_id) references {self.scales_tab}(id))"
                )

    def __del__(self):
        self.connection.close()

    def new(self, a_params: TemplateParams):
        """
        Добавляет новое измерение в базу без коммита
        :return id новой записи
        """
        self.cursor.execute(
            f"insert into {self.templates_tab}(name, device_name, device_creator, device_system) "
            f"VALUES(?,?,?,?)",
            (a_params.name, a_params.device_name, a_params.device_creator, a_params.device_system)
        )
        # Дублировать шкалы ############################################################################################
        template_id = self.cursor.lastrowid
        return template_id

    def get(self, a_id: int) -> TemplateParams:
        try:
            self.cursor.execute(f"select * from {self.templates_tab} WHERE id={a_id}")
            record = self.cursor.fetchone()

            template_params = (TemplateParams(a_id=record[0], a_name=record[1], a_device_name=record[2],
                                              a_device_creator=record[3], a_device_system=record[4]))

            # Достать шкалы ###########################################################################################

            return template_params
        except Exception as err:
            print(err)

    def save(self, a_params: TemplateParams):
        """
        Обновляет запись и фиксирует изменения в БД
        """
        self.cursor.execute(
            f"update {self.templates_tab} set name = ?, device_name = ?, device_creator = ?, device_system = ?"
            f"where id = '{a_params.id}'",
            (a_params.name, a_params.device_name, a_params.device_creator, a_params.device_system)
        )
        self.connection.commit()

    def cancel(self):
        self.connection.rollback()

    def delete(self, a_id: int):
        with self.connection:
            # Удалить шкалы ##########################################################################################
            # self.cursor.execute(f"delete from {self.points_tab} where template_id = '{template_id}'")

            self.cursor.execute(f"delete from {self.templates_tab} where id = {a_id}")
            return True

    def is_name_exist(self, a_name: str):
        c = self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {self.templates_tab} where name='{a_name}')")
        res = c.fetchone()
        return res[0]

    def is_id_exist(self, a_id: int):
        c = self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {self.templates_tab} where id={a_id})")
        res = c.fetchone()
        return res[0]

    def __iter__(self):
        # Итерация по именам БД
        self.cursor.execute(f"select id, name from {self.templates_tab} order by name")
        return self

    def __next__(self):
        res = self.cursor.fetchone()
        if res is None:
            raise StopIteration
        else:
            return res[0], res[1]
