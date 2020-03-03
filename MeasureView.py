from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QModelIndex, Qt
from PyQt5.QtWidgets import QMessageBox, QMenu
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QWheelEvent

from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from MeasureModel import MeasureModel, PointData
from db_measures import MeasureParams
import calibrator_constants as clb
import qt_utils


class MeasureView:
    def __init__(self, a_table_view: QtWidgets.QTableView, a_measure_config: MeasureParams, a_normalize_value=None,
                 a_init_points=None):

        self.table = a_table_view
        self.measure_config = a_measure_config

        # ################################################################ РАССЧИТАТЬ НОРМИРУЮЩЕЕ ЗНАЧЕНЕ
        self.normalize_value = 1 if a_normalize_value is None else a_normalize_value

        self.measure_model = MeasureModel(a_normalize_value=self.normalize_value,
                                          a_error_limit=self.measure_config.device_class,
                                          a_signal_type=self.measure_config.signal_type,
                                          a_init_points=a_init_points, a_parent=self)

        self.table.setModel(self.measure_model)
        self.table.setItemDelegate(NonOverlappingDoubleClick(self))
        self.table.customContextMenuRequested.connect(self.show_table_custom_menu)

        self.table.setColumnHidden(MeasureModel.Column.FREQUENCY, clb.is_dc_signal[self.measure_config.signal_type])

        for point in self.measure_config.points:
            self.measure_model.appendPoint(PointData(a_point=point.amplitude, a_frequency=point.frequency))

        self.header_context = qt_utils.TableHeaderContextMenu(self, self.ui.measure_table)

    def show_table_custom_menu(self, a_position: QtCore.QPoint):
        menu = QMenu(self)
        copy_cell_act = menu.addAction("Копировать")
        copy_cell_act.triggered.connect(self.copy_cell_text_to_clipboard)
        menu.popup(self.ui.measure_table.viewport().mapToGlobal(a_position))

    def removeSelectedRows(self):
        pass


    def copy_cell_text_to_clipboard(self):
        text = self.measure_model.getText(self.ui.measure_table.selectionModel().currentIndex())
        if text:
            QtWidgets.QApplication.clipboard().setText(text)