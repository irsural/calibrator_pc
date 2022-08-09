from typing import List, Iterable
import sqlite3

from constants import DeviceSystem, Scale
from irspy import utils


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

        with self.connection:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS templates "
                "(id integer primary key autoincrement, name text, device_name text, device_creator text, "
                "device_system integer)"
            )

            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS scales "
                "(id integer primary key autoincrement, scale_number int, points text, template_id int,"
                "foreign key (template_id) references templates(id))"
            )

            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS limits "
                "(id integer primary key autoincrement, scale_limit real, device_class real, signal_type int,"
                "frequency text, scale_id int, "
                "foreign key (scale_id) references scales(id))"
            )

    def __del__(self):
        self.connection.close()

    def new(self, a_params: TemplateParams):
        """
        Добавляет новое измерение в базу без коммита
        ИЗМЕНЯЕТ a_prams.id !!!
        """
        self.cursor.execute(
            "insert into templates(name, device_name, device_creator, device_system) "
            "values (?,?,?,?)",
            (a_params.name, a_params.device_name, a_params.device_creator, a_params.device_system)
        )
        a_params.id = self.cursor.lastrowid

        for scale in a_params.scales:
            self.new_scale(a_params.id, scale)

    @utils.exception_decorator_print
    def get(self, a_id: int) -> TemplateParams:
        self.cursor.execute("select * from templates WHERE id={0}".format(a_id))
        template_rec = self.cursor.fetchone()

        template_id = template_rec[0]

        self.cursor.execute("select * from scales WHERE template_id={0}".format(template_id))
        scales_recs = self.cursor.fetchall()

        template_scales = []
        for s_id, s_number, s_points, _ in scales_recs:
            points = s_points.split(';')
            scale_points = [float(p) for p in points] if points[0] else []

            self.cursor.execute("select * from limits WHERE scale_id={0}".format(s_id))
            scale_limits = [Scale.Limit(*rec[0:-1]) for rec in self.cursor.fetchall()]

            template_scales.append(Scale(s_id, s_number, scale_points, scale_limits))

        assert template_scales, "Every template must have at least one scale!!!"

        template_params = (TemplateParams(a_id=template_rec[0], a_name=template_rec[1],
                                          a_device_name=template_rec[2], a_device_creator=template_rec[3],
                                          a_device_system=template_rec[4], a_scales=template_scales))

        return template_params

    def save(self, a_params: TemplateParams):
        """
        Обновляет запись и фиксирует изменения в БД
        """
        self.cursor.executemany(
            "update scales set scale_number = ?, points = ? where id = ?",
            ((scale.number, ';'.join((str(p) for p in scale.points)), scale.id) for scale in a_params.scales)
        )

        self.cursor.execute(
            "update templates set name = ?, device_name = ?, device_creator = ?, device_system = ?"
            "where id = {0}".format(a_params.id),
            (a_params.name, a_params.device_name, a_params.device_creator, a_params.device_system)
        )
        self.connection.commit()

    def cancel(self):
        self.connection.rollback()

    def delete(self, a_params: TemplateParams):
        with self.connection:
            scale_ids = ','.join([str(scale.id) for scale in a_params.scales])

            self.cursor.execute("delete from limits where scale_id in ({0})".format(scale_ids))
            self.cursor.execute("delete from scales where id in ({0})".format(scale_ids))
            self.cursor.execute("delete from templates where id = {0}".format(a_params.id))
            return True

    def new_scale(self, a_template_id: int, a_scale=None):
        scale = a_scale if a_scale is not None else Scale()

        self.cursor.execute("insert into scales (scale_number, points, template_id) "
                            "values (?, ?, ?)", (scale.number, ';'.join([str(p) for p in scale.points]),
                                                 a_template_id))

        scale.id = self.cursor.lastrowid

        for limit in scale.limits:
            self.new_limit(scale.id, limit)

        return scale

    def delete_scale(self, a_scale_id: int):
        self.cursor.execute("delete from limits where scale_id in ({0})".format(a_scale_id))

        self.cursor.execute("delete from scales where id in ({0})".format(a_scale_id))

    def new_limit(self, a_scale_id: int, a_limit: Scale.Limit = None):
        limit = a_limit if a_limit is not None else Scale.Limit()

        self.cursor.execute(
            "insert into limits (scale_limit, device_class, signal_type, frequency, scale_id) "
            "values (?, ?, ?, ?, ?)", (limit.limit, limit.device_class, limit.signal_type, limit.frequency, a_scale_id)
        )

        limit.id = self.cursor.lastrowid

        return limit

    def update_limit(self, a_limit: Scale.Limit):
        self.cursor.execute(
            "update limits set scale_limit = ?, device_class = ?, signal_type = ?, frequency = ? "
            "where id = ?",
            (a_limit.limit, a_limit.device_class, a_limit.signal_type, a_limit.frequency, a_limit.id)
        )

    def get_limits(self, a_scale_id):
        self.cursor.execute("select * from limits where scale_id = {0}".format(a_scale_id))
        return [Scale.Limit(*rec[:-1]) for rec in self.cursor.fetchall()]

    def delete_limits(self, a_deleted_ids: Iterable[int]):
        self.cursor.execute(
            "delete from limits where id in ({0})".format(','.join(str(d_id) for d_id in a_deleted_ids))
        )

    def is_name_exist(self, a_name: str):
        c = self.cursor.execute("SELECT EXISTS(SELECT 1 FROM templates where name='{0}')".format(a_name))
        res = c.fetchone()
        return res[0]

    def is_id_exist(self, a_id: int):
        c = self.cursor.execute("SELECT EXISTS(SELECT 1 FROM templates where id={0})".format(a_id))
        res = c.fetchone()
        return res[0]

    def __iter__(self):
        # Итерация по именам БД
        self.cursor.execute("select id, name from templates order by name")
        return self

    def __next__(self):
        res = self.cursor.fetchone()
        if res is None:
            raise StopIteration
        else:
            return res[0], res[1]
