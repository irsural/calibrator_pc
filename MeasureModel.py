import enum
from typing import List, Iterable

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot
from PyQt5.QtGui import QBrush, QColor

from db_measures import MeasuredPoint
import calibrator_constants as clb
import utils


class PointData:
    class ApproachSide(enum.IntEnum):
        UP = 0
        DOWN = 1

    def __init__(self, a_point=0., a_frequency=0., a_value=0., a_approach_side=ApproachSide.UP,
                 a_scale_point=0.):
        self.scale_point = a_scale_point
        self.amplitude = a_point
        self.frequency = a_frequency
        self.value = a_value
        self.approach_side = a_approach_side

    def round_data(self):
        self.scale_point = round(self.scale_point, 9)
        self.amplitude = round(self.amplitude, 9)
        self.frequency = round(self.frequency, 9)
        self.value = round(self.value, 9)
        self.approach_side = round(self.approach_side, 9)

    def __str__(self):
        return "Point: {0}\n" \
            "Frequency: {1}" \
            "Value: {2}\n" \
            "Side: {3}".format(self.amplitude, self.frequency, self.value, self.approach_side.name)


class MeasureModel(QAbstractTableModel):
    class Column(enum.IntEnum):
        SCALE_POINT = 0
        AMPLITUDE = 1
        FREQUENCY = 2
        UP_VALUE = 3
        UP_DEVIATION = 4
        UP_DEVIATION_PERCENT = 5
        DOWN_VALUE = 6
        DOWN_DEVIATION = 7
        DOWN_DEVIATION_PERCENT = 8
        VARIATION = 9
        COUNT = 10

    enum_to_column_header = {
        Column.SCALE_POINT: "Отметка\nшкалы",
        Column.AMPLITUDE: "Амплитуда",
        Column.FREQUENCY: "Частота, Гц",
        Column.UP_VALUE: "Значение\nсверху",
        Column.UP_DEVIATION: "Отклонение\nсверху",
        Column.UP_DEVIATION_PERCENT: "Отклонение\nсверху, %",
        Column.DOWN_VALUE: "Значение\nснизу",
        Column.DOWN_DEVIATION: "Отклонение\nснизу",
        Column.DOWN_DEVIATION_PERCENT: "Отклонение\nснизу, %",
        Column.VARIATION: "Вариация",
        Column.COUNT: ">>>>>>ОШИБКА<<<<<<"
    }

    __side_to_value_column = {
        PointData.ApproachSide.DOWN: Column.DOWN_VALUE,
        PointData.ApproachSide.UP: Column.UP_VALUE
    }
    __side_to_error_column = {
        PointData.ApproachSide.DOWN: Column.DOWN_DEVIATION,
        PointData.ApproachSide.UP: Column.UP_DEVIATION
    }
    __side_to_error_percent_column = {
        PointData.ApproachSide.DOWN: Column.DOWN_DEVIATION_PERCENT,
        PointData.ApproachSide.UP: Column.UP_DEVIATION_PERCENT
    }

    def __init__(self, a_normalize_value, a_error_limit, a_signal_type, a_init_points: List[MeasuredPoint],
                 a_parent=None):
        super().__init__(a_parent)

        self.__row_count = 0
        self.__column_count = MeasureModel.Column.COUNT
        self.__raw_columns = (MeasureModel.Column.SCALE_POINT, MeasureModel.Column.FREQUENCY,
                              MeasureModel.Column.DOWN_DEVIATION_PERCENT, MeasureModel.Column.UP_DEVIATION_PERCENT)

        self.__points = []

        self.AVERAGE_SUM_IDX = 0
        self.AVERAGE_COUNT_IDX = 1
        self.__average_data = [[[0, 1]] * MeasureModel.Column.COUNT]

        self.signal_type = a_signal_type
        self.value_to_user = utils.value_to_user_with_units(clb.signal_type_to_units[self.signal_type])
        self.normalize_value = a_normalize_value
        self.error_limit = a_error_limit
        self.__good_color = QColor(0, 255, 0, 127)
        self.__bad_color = QColor(255, 0, 0, 127)

        assert a_init_points is not None, "a_init_points must not be None!"

        if a_init_points:
            # Формат a_init_points - кортеж, который формируется в self.exportPoints
            for s_p, a, f, up_v, down_v in a_init_points:
                self.appendPoint(PointData(a_scale_point=s_p, a_point=a, a_frequency=f, a_value=up_v,
                                           a_approach_side=PointData.ApproachSide.UP), a_average=False)

                self.appendPoint(PointData(a_scale_point=s_p, a_point=a, a_frequency=f, a_value=down_v,
                                           a_approach_side=PointData.ApproachSide.DOWN), a_average=False)

    def appendPoint(self, a_point_data: PointData, a_average: bool) -> int:
        """
        Добавляет точку в таблицу
        :param a_point_data: Данные точки
        :param a_average: Если равно True, то существующее значение не перезаписывается, а усредняется
        """
        a_point_data.amplitude = clb.bound_amplitude(a_point_data.amplitude, self.signal_type)
        a_point_data.frequency = clb.bound_frequency(a_point_data.frequency, self.signal_type)
        a_point_data.round_data()

        value_column = self.__side_to_value_column[a_point_data.approach_side]
        value = a_point_data.value

        row_idx = self.__find_point(a_point_data.amplitude, a_point_data.frequency)
        point_row = self.rowCount() if row_idx is None else row_idx

        if point_row == self.rowCount():
            assert not a_average, "appendPoint must be called only for existing points"
            # Добавляемой точки еще нет в списке
            point_data = [a_point_data.scale_point, a_point_data.amplitude, a_point_data.frequency, 0, 0, 0, 0, 0, 0, 0]
            assert len(point_data) == MeasureModel.Column.COUNT, "Размер point_data не соответствует количеству " \
                                                                 "колонок таблицы"
            self.__average_data += [[[a_point_data.amplitude, 1]] * MeasureModel.Column.COUNT]

            new_row = self.rowCount()
            self.beginInsertRows(QModelIndex(), new_row, new_row)
            self.__points.append(point_data)
            self.endInsertRows()
        elif a_average:
            self.__average_data[point_row][value_column][self.AVERAGE_SUM_IDX] += value
            self.__average_data[point_row][value_column][self.AVERAGE_COUNT_IDX] += 1

            value = self.__average_data[point_row][value_column][self.AVERAGE_SUM_IDX] / \
                self.__average_data[point_row][value_column][self.AVERAGE_COUNT_IDX]

        if not a_average:
            self.__average_data[point_row][self.__side_to_value_column[a_point_data.approach_side]] = [value, 1]

        self.setData(self.index(point_row, value_column), str(value))
        self.__recalculate_parameters(point_row, a_point_data.approach_side)
        return point_row

    def getPointByRow(self, a_row_idx):
        if len(self.__points) < a_row_idx:
            return None
        else:
            return self.__points[a_row_idx][self.Column.AMPLITUDE]

    def exportPoints(self) -> List[MeasuredPoint]:
        exported_points = [MeasuredPoint(scale_point=row[MeasureModel.Column.SCALE_POINT],
                                         amplitude=row[MeasureModel.Column.AMPLITUDE],
                                         frequency=row[MeasureModel.Column.FREQUENCY],
                                         up_value=row[MeasureModel.Column.UP_VALUE],
                                         down_value=row[MeasureModel.Column.DOWN_VALUE])
                           for row in self.__points]
        return exported_points

    def exportByColumns(self, a_columns: Iterable) -> Iterable[Iterable]:
        table_data = []
        for row in range(self.rowCount()):
            table_data.append([self.data(QModelIndex(self.index(row, column))) for column in a_columns])
        return table_data

    def isPointMeasured(self, a_point: float, a_frequency: float, a_approach_side: PointData.ApproachSide) -> bool:
        """
        Проверяет, есть ли точка в массиве, если точка есть, то проверяет ее состояние (входит в погрешность или нет)
        Если точки нет, или она не входит в погрешность, возвращает False, иначе возвращает True
        :param a_frequency: Частота точки
        :param a_approach_side: Сторона подхода к точке
        :param a_point: Значение точки
        :return: bool
        """
        row_idx = self.__find_point(a_point, a_frequency)
        if row_idx is None:
            return False
        else:
            return self.isPointMeasuredByRow(row_idx, a_approach_side)
            # row_data = self.__points[row_idx]
            # if self.isPointMeasuredByRow(row_idx, a_approach_side):
                # return abs(row_data[self.__side_to_error_percent_column[a_approach_side]]) <= self.error_limit
            # else:
            #     return False

    def __find_point(self, a_point: float, a_frequency: float):
        for idx, row_data in enumerate(self.__points):
            if a_point == row_data[self.Column.AMPLITUDE] and row_data[self.Column.FREQUENCY] == a_frequency:
                return idx
        return None

    def isPointMeasuredByRow(self, a_point_row, a_approach_side: PointData.ApproachSide):
        data_row = self.__points[a_point_row]

        val, err, err_percent = (self.__side_to_value_column[a_approach_side],
                                 self.__side_to_error_column[a_approach_side],
                                 self.__side_to_error_percent_column[a_approach_side])

        if data_row[val] == 0 and data_row[err] == 0 and data_row[err_percent] == 0:
            return False
        else:
            return True

    def __get_cell_color(self, a_row, a_column):
        if a_column in (self.Column.UP_VALUE, self.Column.DOWN_VALUE):
            approach_side = PointData.ApproachSide.UP if a_column == self.Column.UP_VALUE \
                else PointData.ApproachSide.DOWN

            if self.isPointMeasuredByRow(a_row, approach_side):
                if abs(self.__points[a_row][self.__side_to_error_percent_column[approach_side]]) <= self.error_limit:
                    # Если отклонение в процентах не превышает предела погрешности
                    return QVariant(QBrush(self.__good_color))
                else:
                    return QVariant(QBrush(self.__bad_color))
            else:
                return QVariant(QBrush(QColor(Qt.white)))
        else:
            return QVariant(QBrush(QColor(Qt.white)))

    def __recalculate_parameters(self, a_row_idx, a_approach_size: PointData.ApproachSide):
        point = self.__points[a_row_idx][self.Column.AMPLITUDE]
        value = self.__points[a_row_idx][self.__side_to_value_column[a_approach_size]]
        if point != 0 and value == 0:
            # Если точка добавлена в таблицу, но еще не измерена
            return

        absolute_error = utils.absolute_error(point, value)
        relative_error = utils.relative_error(point, value, self.normalize_value)

        self.setData(self.index(a_row_idx, self.__side_to_error_column[a_approach_size]), str(absolute_error))
        self.setData(self.index(a_row_idx, self.__side_to_error_percent_column[a_approach_size]), str(relative_error))

        down_value = self.__points[a_row_idx][self.Column.DOWN_VALUE]
        up_value = self.__points[a_row_idx][self.Column.UP_VALUE]
        if (down_value != 0) and (up_value != 0):
            self.setData(self.index(a_row_idx, self.Column.VARIATION), str(utils.variation(down_value, up_value)))

    def set_device_class(self, a_class: float):
        self.error_limit = a_class
        for row in range(self.rowCount()):
            self.__recalculate_parameters(row, PointData.ApproachSide.UP)
            self.__recalculate_parameters(row, PointData.ApproachSide.DOWN)

        self.dataChanged.emit(self.index(0, MeasureModel.Column.DOWN_VALUE),
                              self.index(self.rowCount(), MeasureModel.Column.DOWN_VALUE))
        self.dataChanged.emit(self.index(0, MeasureModel.Column.UP_VALUE),
                              self.index(self.rowCount(), MeasureModel.Column.UP_VALUE))

    def rowCount(self, parent=QModelIndex()):
        return len(self.__points)

    def columnCount(self, parent=QModelIndex()):
        return self.__column_count

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Vertical:
            return section + 1
        else:
            return self.enum_to_column_header[self.Column(section)]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or (len(self.__points) < index.row()) or \
                (role != Qt.DisplayRole and role != Qt.EditRole and role != Qt.BackgroundRole and role != Qt.UserRole):
            return QVariant()
        if role == Qt.UserRole:
            return self.__average_data[index.row()][index.column()][self.AVERAGE_COUNT_IDX]
        elif role == Qt.BackgroundRole:
            return self.__get_cell_color(index.row(), index.column())
        else:
            value = self.__points[index.row()][index.column()]
            if index.column() not in self.__raw_columns:
                value = self.value_to_user(value)
            else:
                value = utils.float_to_string(value)
            return value

    def setData(self, index: QModelIndex, value: str, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole or self.rowCount() <= index.row():
            return False
        try:
            float_value = utils.parse_input(value)

            if index.column() in (self.Column.AMPLITUDE, self.Column.DOWN_VALUE, self.Column.UP_VALUE):
                float_value = clb.bound_amplitude(float_value, self.signal_type)
            elif index.column() == self.Column.FREQUENCY:
                float_value = clb.bound_frequency(float_value, self.signal_type)

            self.__points[index.row()][index.column()] = float_value
            self.dataChanged.emit(index, index)

            if index.column() in (self.Column.AMPLITUDE, self.Column.DOWN_VALUE, self.Column.UP_VALUE):
                if index.column() != self.Column.DOWN_VALUE:
                    self.__recalculate_parameters(index.row(), PointData.ApproachSide.UP)

                if index.column() != self.Column.UP_VALUE:
                    self.__recalculate_parameters(index.row(), PointData.ApproachSide.DOWN)

                if index.column() == self.Column.AMPLITUDE:
                    # Это нужно, чтобы цвета ячеек Нижнее значение и Верхнее значение обновлялись сразу после изменения
                    # ячейки Поверяемая точка
                    up_value_index = self.index(index.row(), self.Column.UP_VALUE)
                    down_value_index = self.index(index.row(), self.Column.DOWN_VALUE)

                    self.dataChanged.emit(up_value_index, up_value_index)
                    self.dataChanged.emit(down_value_index, down_value_index)

            return True
        except ValueError:
            return False

    @pyqtSlot(list)
    def removeSelected(self, a_row_indexes: list):
        # Работает только для последовательного выделения
        self.beginRemoveRows(QModelIndex(), a_row_indexes[0], a_row_indexes[-1])
        del self.__points[a_row_indexes[0]:a_row_indexes[-1] + 1]
        del self.__average_data[a_row_indexes[0]:a_row_indexes[-1] + 1]
        self.endRemoveRows()

    @staticmethod
    def getText(index: QModelIndex):
        if index.isValid():
            return index.data()
        else:
            return ""

    def flags(self, index):
        item_flags = super().flags(index)
        if index.isValid():
            if index.column() in (self.Column.SCALE_POINT, self.Column.AMPLITUDE, self.Column.FREQUENCY,
                                  self.Column.UP_VALUE, self.Column.DOWN_VALUE):
                item_flags |= Qt.ItemIsEditable
        return item_flags
