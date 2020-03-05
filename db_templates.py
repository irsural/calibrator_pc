from typing import List
import sqlite3

import calibrator_constants as clb
from constants import DeviceSystem, MeasuredPoint, Scale
import utils


class TemplateParams:
    def __init__(self, a_id=0, a_name="Новый шаблон", a_device_name="", a_device_creator="",
                 a_device_system=DeviceSystem.MAGNETOELECTRIC, a_scales: List[Scale] = None):
        self.id = a_id
        self.name = a_name
        self.device_name = a_device_name
        self.device_creator = a_device_creator
        self.device_system = a_device_system
        self.scales = a_scales if a_scales else [Scale()]


class TemplatesDB:
    def __init__(self, a_db_name="templates.db"):
        self.connection = sqlite3.connect(a_db_name)
        self.cursor = self.connection.cursor()

        self.templates_tab = "templates"
        self.scales_tab = "scales"
        self.scale_points = "scale_points"
        self.limits_tab = "limits"

        with self.connection:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.templates_tab} "
                f"(id integer primary key autoincrement, name text, device_name text, device_creator text, "
                f"device_system integer)"
            )

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.scales_tab} "
                f"(id integer primary key autoincrement, scale_number int, template_id int,"
                f"foreign key (template_id) references {self.templates_tab}(id))"
            )

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.scale_points} "
                f"(id integer primary key autoincrement, point real, scale_id int, "
                f"foreign key (scale_id) references {self.scales_tab}(id))"
            )

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.limits_tab} "
                f"(id integer primary key autoincrement, scale_limit real, device_class real, signal_type int,"
                f"frequency text, scale_id int, "
                f"foreign key (scale_id) references {self.scales_tab}(id))"
            )

    def __del__(self):
        self.connection.close()

    def new(self, a_params: TemplateParams):
        """
        Добавляет новое измерение в базу без коммита
        ИЗМЕНЯЕТ a_prams.id !!!
        """
        self.cursor.execute(
            f"insert into {self.templates_tab}(name, device_name, device_creator, device_system) "
            f"values (?,?,?,?)",
            (a_params.name, a_params.device_name, a_params.device_creator, a_params.device_system)
        )
        a_params.id = self.cursor.lastrowid

        for scale in a_params.scales:
            self.new_scale(a_params.id, scale)

    def get(self, a_id: int) -> TemplateParams:
        try:
            self.cursor.execute(f"select * from {self.templates_tab} WHERE id={a_id}")
            template_rec = self.cursor.fetchone()

            template_id = template_rec[0]

            self.cursor.execute(f"select * from {self.scales_tab} WHERE template_id={template_id}")
            scales_recs = self.cursor.fetchall()

            template_scales = []
            for s_id, s_number, _ in scales_recs:

                self.cursor.execute(f"select point from {self.scale_points} WHERE scale_id={s_id} order by id")
                scale_points: List[float] = [p for p in self.cursor.fetchall()]

                self.cursor.execute(f"select * from {self.limits_tab} WHERE scale_id={s_id}")
                scale_limits: List[Scale.Limit] = [Scale.Limit(*rec[0:-1]) for rec in self.cursor.fetchall()]

                template_scales.append(Scale(s_id, s_number, scale_points, scale_limits))

                print(template_scales[-1])

            assert template_scales, "Every template must have at least one scale!!!"

            template_params = (TemplateParams(a_id=template_rec[0], a_name=template_rec[1],
                                              a_device_name=template_rec[2], a_device_creator=template_rec[3],
                                              a_device_system=template_rec[4], a_scales=template_scales))

            return template_params
        except Exception as err:
            utils.exception_handler(err)

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

    def delete(self, a_params: TemplateParams):
        with self.connection:
            scale_ids = ','.join([str(scale.id) for scale in a_params.scales])

            self.cursor.execute(f"delete from {self.scale_points} where scale_id in ({scale_ids})")
            self.cursor.execute(f"delete from {self.limits_tab} where scale_id in ({scale_ids})")

            self.cursor.execute(f"delete from {self.scales_tab} where id in ({scale_ids})")

            self.cursor.execute(f"delete from {self.templates_tab} where id = {a_params.id}")
            return True

    def new_scale(self, a_template_id: int, a_scale=None):
        scale = a_scale if a_scale is not None else Scale()

        self.cursor.execute(f"insert into {self.scales_tab} (scale_number, template_id) "
                            f"values (?, ?)", (scale.number, a_template_id))

        scale.id = self.cursor.lastrowid

        self.cursor.executemany(f"insert into {self.scale_points} (point, scale_id) "
                                f"values (?, ?)", [(p, scale.id) for p in scale.points])
        for limit in scale.limits:
            self.cursor.execute(
                f"insert into {self.limits_tab} (scale_limit, signal_type, device_class, frequency, scale_id) "
                f"values (?, ?, ?, ?, {scale.id})",
                (limit.limit, limit.signal_type, limit.device_class, limit.frequency)
            )
        return scale

    def delete_scale(self, a_scale_id: int):
        self.cursor.execute(f"delete from {self.scale_points} where scale_id in ({a_scale_id})")
        self.cursor.execute(f"delete from {self.limits_tab} where scale_id in ({a_scale_id})")

        self.cursor.execute(f"delete from {self.scales_tab} where id in ({a_scale_id})")

    def update_scale_number(self, a_scale_id, a_new_idx):
        self.cursor.execute(f"update {self.scales_tab} set scale_number = {a_new_idx} where id = {a_scale_id}")

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
