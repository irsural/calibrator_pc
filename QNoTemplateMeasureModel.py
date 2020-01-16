from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot
import enum


class PointData:

    def __init__(self, a_point=0., a_value=0., a_prev_value=0):
        self.point = a_point
        self.value = a_value
        self.prev_value = a_prev_value

    def __str__(self):
        return f"Point: {self.point}\n" \
            f"Value: {self.value}\n" \
            f"Prev value: {self.prev_value}\n"


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

    def appendPoint(self, a_point_data: PointData):
        # if

        point_data = [str(a_point_data.point), str(a_point_data.value), "0", "0", str(a_point_data.value), "0", "0"]

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
