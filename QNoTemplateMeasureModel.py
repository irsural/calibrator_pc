import enum
from typing import List

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot
from PyQt5.QtGui import QBrush, QColor

import calibrator_constants as clb
import utils

class PointData:
    class ApproachSide(enum.IntEnum):
        UP = 0
        DOWN = 1

    def __init__(self, a_point=0., a_frequency=0., a_value=0., a_prev_value=0, a_normalize_value=0):
        self.point = a_point
        self.frequency = a_frequency
        self.value = a_value
        self.prev_value = a_prev_value
        self.approach_side = self.ApproachSide.UP
        self.normalize_value = a_normalize_value

    def __str__(self):
        return f"Point: {self.point}\n" \
            f"Frequency: {self.frequency}" \
            f"Value: {self.value}\n" \
            f"Prev value: {self.prev_value}\n" \
            f"Prev value: {self.prev_value}\n" \
            f"Side: {self.approach_side.name}" \
            f"Normalize: {self.normalize_value}"


class QNoTemplateMeasureModel(QAbstractTableModel):
    class Column(enum.IntEnum):
        POINT = 0
        FREQUENCY = 1
        UP_VALUE = 2
        UP_DEVIATION = 3
        UP_DEVIATION_PERCENT = 4
        DOWN_VALUE = 5
        DOWN_DEVIATION = 6
        DOWN_DEVIATION_PERCENT = 7
        VARIATION = 8
        COUNT = 9

    enum_to_column_header = {
        Column.POINT: "Поверяемая\nточка",
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

    def __init__(self, a_normalize_value, a_error_limit, a_signal_type, a_parent=None):
        super().__init__(a_parent)

        self.__row_count = 0
        self.__column_count = self.Column.COUNT
        self.__raw_columns = self.Column.FREQUENCY, self.Column.DOWN_DEVIATION_PERCENT, self.Column.UP_DEVIATION_PERCENT

        self.__points: List[List[float]] = []

        self.signal_type = a_signal_type
        self.value_to_user = utils.value_to_user_with_units(clb.signal_type_to_units[self.signal_type])
        self.normalize_value = a_normalize_value
        self.error_limit = a_error_limit
        self.__good_color = QColor(0, 255, 0, 127)
        self.__bad_color = QColor(255, 0, 0, 127)

    def appendPoint(self, a_point_data: PointData) -> int:
        row_idx = self.__find_point(a_point_data.point, a_point_data.frequency)
        point_row = self.rowCount() if row_idx is None else row_idx

        if point_row == self.rowCount():
            # Добавляемой точки еще нет в списке
            point_data = [a_point_data.point, a_point_data.frequency, 0, 0, 0, 0, 0, 0, 0]
            assert len(point_data) == self.Column.COUNT, "Размер point_data не соответствует количеству колонок таблицы"

            new_row = self.rowCount()
            self.beginInsertRows(QModelIndex(), new_row, new_row)
            self.__points.append(point_data)
            self.endInsertRows()

        value_column = self.__side_to_value_column[a_point_data.approach_side]
        self.setData(self.index(point_row, value_column), str(a_point_data.value))
        self.__recalculate_parameters(point_row, a_point_data.approach_side, a_point_data.point, a_point_data.value)
        return point_row

    def getPointByRow(self, a_row_idx):
        if len(self.__points) < a_row_idx:
            return None
        else:
            return self.__points[a_row_idx][self.Column.POINT]

    def exportPoints(self):
        return tuple(self.__points)

    def isPointGood(self, a_point: float, a_freqyency: float, a_approach_side: PointData.ApproachSide) -> bool:
        """
        Проверяет, есть ли точка в массиве, если точка есть, то проверяет ее состояние (входит в погрешность или нет)
        Если точки нет, или она не входит в погрешность, возвращает False, иначе возвращает True
        :param a_freqyency: Частота точки
        :param a_approach_side: Сторона подхода к точке
        :param a_point: Значение точки
        :return: bool
        """
        row_idx = self.__find_point(a_point, a_freqyency)
        if row_idx is None:
            return False
        else:
            row_data = self.__points[row_idx]
            if self.isPointMeasured(row_idx, a_approach_side):
                return abs(row_data[self.__side_to_error_percent_column[a_approach_side]]) <= self.error_limit
            else:
                return False

    def __find_point(self, a_point: float, a_frequency: float):
        for idx, row_data in enumerate(self.__points):
            if a_point == row_data[self.Column.POINT] and row_data[self.Column.FREQUENCY] == a_frequency:
                return idx
        return None

    def isPointMeasured(self, a_point_row, a_approach_side: PointData.ApproachSide):
        data_row = self.__points[a_point_row]

        val, err, err_percent = self.__side_to_value_column[a_approach_side], \
                                self.__side_to_error_column[a_approach_side], \
                                self.__side_to_error_percent_column[a_approach_side]

        if data_row[val] == 0 and data_row[err] == 0 and data_row[err_percent] == 0:
            return False
        else:
            return True

    def __get_cell_color(self, a_row, a_column):
        if a_column in (self.Column.UP_VALUE, self.Column.DOWN_VALUE):
            approach_side = PointData.ApproachSide.UP if a_column == self.Column.UP_VALUE \
                else PointData.ApproachSide.DOWN

            if self.isPointMeasured(a_row, approach_side):
                if abs(self.__points[a_row][self.__side_to_error_percent_column[approach_side]]) <= self.error_limit:
                    # Если отклонение в процентах не превышает предела погрешности
                    return QVariant(QBrush(self.__good_color))
                else:
                    return QVariant(QBrush(self.__bad_color))
        else:
            return QVariant(QBrush(QColor(Qt.white)))

    def __recalculate_parameters(self, a_row_idx, a_approach_size: PointData.ApproachSide, a_point, a_value):
        if a_point != 0 and a_value == 0:
            # Если точка добавлена в таблицу, но еще не измерена
            return

        absolute_error = utils.absolute_error(a_point, a_value)
        relative_error = utils.relative_error(a_point, a_value, self.normalize_value)

        self.setData(self.index(a_row_idx, self.__side_to_error_column[a_approach_size]), str(absolute_error))
        self.setData(self.index(a_row_idx, self.__side_to_error_percent_column[a_approach_size]), str(relative_error))

        down_value = self.__points[a_row_idx][self.Column.DOWN_VALUE]
        up_value = self.__points[a_row_idx][self.Column.UP_VALUE]
        if (down_value != 0) and (up_value != 0):
            self.setData(self.index(a_row_idx, self.Column.VARIATION), str(utils.variation(down_value, up_value)))

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
                (role != Qt.DisplayRole and role != Qt.EditRole and role != Qt.BackgroundRole):
            return QVariant()

        if role == Qt.BackgroundRole:
            return self.__get_cell_color(index.row(), index.column())
        else:
            value: float = self.__points[index.row()][index.column()]
            if index.column() not in self.__raw_columns:
                value = self.value_to_user(value)
            return value

    def setData(self, index: QModelIndex, value: str, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole or self.rowCount() <= index.row():
            return False
        try:
            float_value = utils.parse_input(value)

            if index.column() in (self.Column.POINT, self.Column.DOWN_VALUE, self.Column.UP_VALUE):
                float_value = clb.bound_amplitude(float_value, self.signal_type)
            elif index.column() == self.Column.FREQUENCY:
                float_value = clb.bound_frequency(float_value, self.signal_type)

            self.__points[index.row()][index.column()] = float_value
            self.dataChanged.emit(index, index)

            if index.column() == self.Column.POINT:
                self.__recalculate_parameters(index.row(), PointData.ApproachSide.UP, float_value,
                                              self.__points[index.row()][self.Column.UP_VALUE])
                self.__recalculate_parameters(index.row(), PointData.ApproachSide.DOWN, float_value,
                                              self.__points[index.row()][self.Column.DOWN_VALUE])

            return True
        except ValueError:
            return False

    @pyqtSlot(list)
    def removeSelected(self, a_row_indexes: list):
        # Работает только для последовательного выделения
        self.beginRemoveRows(QModelIndex(), a_row_indexes[0], a_row_indexes[-1])
        del self.__points[a_row_indexes[0]:a_row_indexes[-1] + 1]
        self.endRemoveRows()

    def flags(self, index):
        item_flags = super().flags(index)
        if index.isValid():
            if index.column() == self.Column.POINT or index.column() == self.Column.FREQUENCY:
                item_flags |= Qt.ItemIsEditable
            # if index.column() in (self.Column.UP_VALUE, self.Column.DOWN_VALUE):
            #     item_flags &= ~Qt.ItemIsSelectable
        return item_flags
