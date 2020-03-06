from PyQt5 import QtCore, QtGui, QtWidgets

from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from MeasureModel import MeasureModel, PointData
from db_measures import Measure
import calibrator_constants as clb
import qt_utils


class MeasureView:
    def __init__(self, a_table_view: QtWidgets.QTableView, a_measure_config: Measure, a_normalize_value=0):

        self.table = a_table_view
        self.measure_config = a_measure_config

        if a_normalize_value != 0:
            self.normalize_value = a_normalize_value
        elif self.measure_config.points:
            self.normalize_value = max(self.measure_config.points, key=lambda p: p.amplitude).amplitude
        else:
            self.normalize_value = 1

        self.measure_model = MeasureModel(a_normalize_value=self.normalize_value,
                                          a_error_limit=self.measure_config.device_class,
                                          a_signal_type=self.measure_config.signal_type,
                                          a_init_points=self.measure_config.points, a_parent=self.table)

        assert self.measure_config.points == self.measure_model.exportPoints(), \
            f"Points were inited with errors:\n{self.measure_config.points}\n{self.measure_model.exportPoints()}"

        self.table.setModel(self.measure_model)
        self.table.setItemDelegate(NonOverlappingDoubleClick(self.table))
        self.table.customContextMenuRequested.connect(self.show_table_custom_menu)
        self.table.setColumnHidden(MeasureModel.Column.FREQUENCY, clb.is_dc_signal[self.measure_config.signal_type])

        self.header_context = qt_utils.TableHeaderContextMenu(self.table, self.table)

    def __del__(self):
        print("MeasureView deleted")

    def close(self):
        # Без этого header_context не уничтожится
        self.header_context.delete_connections()

    def show_table_custom_menu(self, a_position: QtCore.QPoint):
        menu = QtWidgets.QMenu(self.table)
        copy_cell_act = menu.addAction("Копировать")
        copy_cell_act.triggered.connect(self.copy_cell_text_to_clipboard)
        menu.popup(self.table.viewport().mapToGlobal(a_position))

    def copy_cell_text_to_clipboard(self):
        text = self.measure_model.getText(self.table.selectionModel().currentIndex())
        if text:
            QtWidgets.QApplication.clipboard().setText(text)

    def remove_selected(self, a_rows: list):
        self.measure_model.removeSelected(a_rows)

    def get_point_by_row(self, a_row: int):
        return self.__get_cell_text(a_row, MeasureModel.Column.POINT)

    def get_frequency_by_row(self, a_row: int):
        return self.__get_cell_text(a_row, MeasureModel.Column.FREQUENCY)

    def __get_cell_text(self, a_row: int, a_column: int):
        index = self.measure_model.index(a_row, a_column)
        return self.measure_model.getText(index)

    def is_point_good(self, a_amplitude: float, a_frequency: float, a_approach_side: PointData.ApproachSide):
        return self.measure_model.isPointGood(a_amplitude, a_frequency, a_approach_side)

    def is_point_measured(self, a_row_idx, a_approach_side: PointData.ApproachSide):
        return self.measure_model.isPointMeasured(a_row_idx, a_approach_side)

    def append(self, a_point: PointData):
        point_row = self.measure_model.appendPoint(a_point)
        self.table.selectRow(point_row)

    def view(self):
        return self.table

    def select_row(self, a_row: int):
        self.table.selectRow(a_row)

    def set_device_class(self, a_class: float):
        self.measure_model.set_device_class(a_class)

    def get_selected_rows(self):
        return self.table.selectionModel().selectedRows()

    def export_points(self):
        return self.measure_model.exportPoints()
