from typing import List
from enum import IntEnum

from PyQt5 import QtCore, QtWidgets

from ui.py.scale_limits_dialog import Ui_Dialog as ScaleLimitsForm
from constants import Scale
import calibrator_constants as clb

import utils


class ScaleLimitsDialog(QtWidgets.QDialog):
    class Column(IntEnum):
        LIMIT = 0
        CLASS = 1
        SIGNAL_TYPE = 2

    def __init__(self, a_limits: List[Scale.Limit], a_parent=None):
        super().__init__(a_parent)

        self.ui = ScaleLimitsForm()
        self.ui.setupUi(self)

        self.limits = a_limits
        self.recover_params(self.limits)

        self.ui.limits_table.itemChanged.connect(self.set_value_to_user)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.reject_button.clicked.connect(self.reject)

    def set_value_to_user(self, a_item: QtWidgets.QTableWidgetItem):
        self.ui.limits_table.blockSignals(True)
        try:
            if a_item.column() == ScaleLimitsDialog.Column.LIMIT:
                value_f = utils.parse_input(a_item.text())
                signal_type = clb.SignalType(
                    self.ui.limits_table.cellWidget(a_item.row(), ScaleLimitsDialog.Column.SIGNAL_TYPE).currentIndex())
                units = clb.signal_type_to_units[signal_type]
                value_f = clb.bound_amplitude(value_f, signal_type)
                value_str = utils.value_to_user_with_units(units)(value_f)

                a_item.setText(value_str)
                a_item.setData(QtCore.Qt.UserRole, value_str)

        except ValueError:
            a_item.setText(a_item.data(QtCore.Qt.UserRole))
        self.ui.limits_table.blockSignals(False)

    def recover_params(self, a_limits: List[Scale.Limit]):
        for limit in a_limits:
            row_idx = self.ui.limits_table.rowCount()
            self.ui.limits_table.insertRow(row_idx)

            units = clb.signal_type_to_units[limit.signal_type]
            self.ui.limits_table.setItem(row_idx, ScaleLimitsDialog.Column.LIMIT,
                                         QtWidgets.QTableWidgetItem(utils.value_to_user_with_units(units)(limit.limit)))

            class_spinbox = QtWidgets.QDoubleSpinBox(self)
            class_spinbox.setDecimals(4)
            class_spinbox.setMinimum(0.001)
            class_spinbox.setMaximum(10)
            class_spinbox.setSingleStep(0.05)
            class_spinbox.setValue(limit.device_class)
            self.ui.limits_table.setCellWidget(row_idx, ScaleLimitsDialog.Column.CLASS, class_spinbox)

            signal_type_combobox = QtWidgets.QComboBox(self)
            for s_t in clb.SignalType:
                signal_type_combobox.addItem(clb.enum_to_signal_type_short[s_t])
            signal_type_combobox.setCurrentIndex(limit.signal_type)
            signal_type_combobox.setProperty("row_in_table", int(row_idx))
            signal_type_combobox.currentIndexChanged.connect(self.signal_type_changed)
            self.ui.limits_table.setCellWidget(row_idx, ScaleLimitsDialog.Column.SIGNAL_TYPE, signal_type_combobox)

    def signal_type_changed(self, a_idx):
        sender_table_row = int(self.sender().property("row_in_table"))
        row_limit_item = self.ui.limits_table.item(sender_table_row, ScaleLimitsDialog.Column.LIMIT)

        value_f = utils.parse_input(row_limit_item.text())
        signal_type = clb.SignalType(a_idx)
        units = clb.signal_type_to_units[signal_type]

        value_str = utils.value_to_user_with_units(units)(value_f)
        row_limit_item.setText(value_str)

    def extract_params(self) -> List[Scale.Limit]:
        scales = []
        for row_idx in range(self.ui.limits_table.rowCount()):
            limit = utils.parse_input(self.ui.limits_table.item(row_idx, ScaleLimitsDialog.Column.LIMIT).text())
            limit_class = self.ui.limits_table.cellWidget(row_idx, ScaleLimitsDialog.Column.CLASS).value()
            signal_type = self.ui.limits_table.cellWidget(row_idx, ScaleLimitsDialog.Column.SIGNAL_TYPE).currentIndex()
            scales.append(Scale.Limit(limit, limit_class, clb.SignalType(signal_type)))
        return scales

    def exec_and_get_limits(self):
        if self.exec() == QtWidgets.QDialog.Accepted:
            return self.extract_params()
        else:
            return None
