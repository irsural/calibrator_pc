import enum

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot

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

    def __init__(self, a_parent=None, a_value_units="А"):
        super().__init__(a_parent)

        self.__row_count = 0
        self.__column_count = self.Column.COUNT
        self.__raw_columns = self.Column.FREQUENCY, self.Column.DOWN_DEVIATION_PERCENT, self.Column.UP_DEVIATION_PERCENT

        self.__points: list[list[float]] = []

        self.value_to_user = utils.value_to_user_with_units(a_value_units)

    def appendPoint(self, a_point_data: PointData):
        row_idx = self.rowCount()
        for idx, row_data in enumerate(self.__points):
            if a_point_data.point == row_data[self.Column.POINT]:
                row_idx = idx
                break

        if row_idx == self.rowCount():
            # Добавляемой точки еще нет в списке
            point_data = [a_point_data.point, a_point_data.frequency, 0, 0, 0, 0, 0, 0, 0]
            assert len(point_data) == self.Column.COUNT, "Размер point_data не соответствует количеству колонок таблицы"

            new_row = self.rowCount()
            self.beginInsertRows(QModelIndex(), new_row, new_row)
            self.__points.append(point_data)
            self.endInsertRows()

        column_idx = self.Column.UP_VALUE if \
            a_point_data.approach_side == PointData.ApproachSide.UP else self.Column.DOWN_VALUE

        self.setData(self.index(row_idx, column_idx), str(a_point_data.value))

        self.__recalculate_parameters(row_idx, a_point_data)

    def __recalculate_parameters(self, a_row_idx, a_point_data: PointData):
        if a_point_data.approach_side == PointData.ApproachSide.DOWN:
            dev_col, dev_col_percent = self.Column.DOWN_DEVIATION, self.Column.DOWN_DEVIATION_PERCENT
        else:
            dev_col, dev_col_percent = self.Column.UP_DEVIATION, self.Column.UP_DEVIATION_PERCENT

        absolute_error = utils.absolute_error(a_point_data.point, a_point_data.value)
        relative_error = utils.relative_error(a_point_data.point, a_point_data.value, a_point_data.normalize_value)

        self.setData(self.index(a_row_idx, dev_col), str(absolute_error))
        self.setData(self.index(a_row_idx, dev_col_percent), str(relative_error))

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
            return section
        return self.enum_to_column_header[section]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid or (len(self.__points) < index.row()) or (role != Qt.DisplayRole and role != Qt.EditRole):
            return QVariant()

        value: float = self.__points[index.row()][index.column()]

        if index.column() not in self.__raw_columns:
            value = self.value_to_user(value)
        return value

    def setData(self, index: QModelIndex, value: str, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole or self.rowCount() <= index.row():
            return False
        try:
            float_value = utils.parse_input(value)
            self.__points[index.row()][index.column()] = float_value
            self.dataChanged.emit(index, index)
            return True
        except ValueError:
            return False

    @pyqtSlot(list)
    def removeSelected(self, a_row_indexes: list):
        self.beginRemoveRows(QModelIndex(), a_row_indexes[0], a_row_indexes[-1])
        del self.__points[a_row_indexes[0]:a_row_indexes[-1]+1]
        self.endRemoveRows()

    def flags(self, index):
        item_flags = super().flags(index)
        if index.isValid():
            if index.column() == self.Column.POINT or index.column() == self.Column.FREQUENCY:
                item_flags |= Qt.ItemIsEditable
        return item_flags
