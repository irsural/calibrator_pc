from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot
import enum


class PointData:
    def __init__(self):
        self.point = 0
        self.up_value = 0
        self.up_deviation = 0
        self.up_deviation_percent = 0
        self.down_value = 0
        self.down_deviation = 0
        self.down_deviation_percent = 0

    def __str__(self):
        return f"Point: {self.point}\n" \
            f"Up: {self.up_value}\n" \
            f"Up dev{self.up_deviation}\n" \
            f"Up dev percent{self.up_deviation_percent}\n" \
            f"Down: {self.down_value}\n" \
            f"Down dev{self.down_deviation}\n" \
            f"Down dev percent{self.down_deviation_percent}\n"


class QNoTemplateMeasureModel(QAbstractTableModel):
    class Column(enum.IntEnum):
        POINT = 0
        UP_VALUE = 1
        UP_DEVIATION = 2
        UP_DEVIATION_PERCENT = 3
        DOWN_VALUE = 4
        DOWN_DEVIATION = 5
        DOWN_DEVIATION_PERCENT = 6
        COUNT = 7

    enum_to_column_header = {
        Column.POINT: "Поверяемая\nточка",
        Column.UP_VALUE: "Значение\nсверху",
        Column.UP_DEVIATION: "Отклонение\nсверху, В",
        Column.UP_DEVIATION_PERCENT: "Отклонение\nсверху, %",
        Column.DOWN_VALUE: "Значение\nснизу",
        Column.DOWN_DEVIATION: "Отклонение\nсверху, В",
        Column.DOWN_DEVIATION_PERCENT: "Отклонение\nсверху, %",
        Column.COUNT: ">>>>>>ОШИБКА<<<<<<"
    }

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.__row_count = 0
        self.__column_count = self.Column.COUNT

        self.__points: list[list[str]] = []

    def appendPoint(self, a_point: PointData):
        point_data = [str(a_point.point), str(a_point.up_value), str(a_point.up_deviation),
                      str(a_point.up_deviation_percent), str(a_point.down_value), str(a_point.down_deviation),
                      str(a_point.down_deviation_percent)
                      ]

        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self.__points.append(point_data)
        self.endInsertRows()

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

        return self.__points[index.row()][index.column()]

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole or self.rowCount() <= index.row():
            return False
        self.__points[index.row()][index.column()] = value
        self.dataChanged.emit(index, index)
        return True

    @pyqtSlot(list)
    def removeSelected(self, a_row_indexes: list):
        self.beginRemoveRows(QModelIndex(), a_row_indexes[0], a_row_indexes[-1])
        del self.__points[a_row_indexes[0]:a_row_indexes[-1]+1]
        self.endRemoveRows()

    def flags(self, index):
        item_flags = super().flags(index)
        if index.isValid():
            if index.column() == self.Column.POINT:
                item_flags |= Qt.ItemIsEditable
        return item_flags
