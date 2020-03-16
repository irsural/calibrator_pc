from typing import Union

from PyQt5 import QtCore, QtWidgets

from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from MeasureModel import MeasureModel, PointData
from db_measures import Measure
import calibrator_constants as clb
import qt_utils


class MeasureView:
    def __init__(self, a_table_view: QtWidgets.QTableView, a_measure_case: Measure.Case):

        self.table = a_table_view
        self.measure_case: Union[Measure.Case, None] = None
        self.measure_model: Union[MeasureModel, None] = None

        # Нужен, чтобы сохранять в него точки, перед self.reset
        self.reset(a_measure_case)

        self.table.setItemDelegate(NonOverlappingDoubleClick(self.table))
        self.table.customContextMenuRequested.connect(self.show_table_custom_menu)

        self.header_context = qt_utils.TableHeaderContextMenu(self.table, self.table)

    def __del__(self):
        print("MeasureView deleted")

    def reset(self, a_case: Measure.Case):
        # Перед сменой кейса сохраняем точки
        self.save_current_points()

        self.measure_case = a_case
        assert a_case.limit != 0, "a_measure_case.limit must not be zero"

        self.measure_model = MeasureModel(a_normalize_value=self.measure_case.limit,
                                          a_error_limit=self.measure_case.device_class,
                                          a_signal_type=self.measure_case.signal_type,
                                          a_init_points=self.measure_case.points, a_parent=self.table)

        assert self.measure_case.points == self.measure_model.exportPoints(), \
            f"Points were inited with errors:\n{self.measure_case.points}\n{self.measure_model.exportPoints()}"

        self.table.setModel(self.measure_model)
        self.table.setColumnHidden(MeasureModel.Column.FREQUENCY, clb.is_dc_signal[self.measure_case.signal_type])

    def save_current_points(self):
        if self.measure_model is not None and self.measure_case is not None:
            self.measure_case.points = self.measure_model.exportPoints()

    def close(self):
        self.save_current_points()
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
        return self.__get_cell_text(a_row, MeasureModel.Column.AMPLITUDE)

    def get_frequency_by_row(self, a_row: int) -> str:
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
