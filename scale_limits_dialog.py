from typing import List
from enum import IntEnum

from PyQt5 import QtCore, QtWidgets

from custom_widgets.QTableDelegates import NonOverlappingDoubleClick
from ui.py.scale_limits_dialog import Ui_Dialog as ScaleLimitsForm
from custom_widgets.EditListDialog import OkCancelDialog, EditedListOnlyNumbers
from constants import Scale
import calibrator_constants as clb

import utils


class FrequencyWidget(QtWidgets.QWidget):
    def __init__(self, a_parent, a_init_frequency: str):
        super().__init__(a_parent)
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.edit = QtWidgets.QLineEdit(a_init_frequency, self)
        self.edit.setReadOnly(True)
        self.edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.edit_button = QtWidgets.QPushButton("...", self)
        self.edit_button.setFixedWidth(30)
        self.edit_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addWidget(self.edit, 0)
        self.main_layout.addWidget(self.edit_button, 0)
        self.setLayout(self.main_layout)

        self.edit_button.clicked.connect(self.open_edit_frequency_dialog)

    def open_edit_frequency_dialog(self):
        frequency_text = self.edit.text()
        current_frequency = frequency_text.split(';') if frequency_text else []
        edit_frequency_dialog = OkCancelDialog(self, "Редактирование частот поверки")

        edit_frequency_widget = EditedListOnlyNumbers(edit_frequency_dialog, tuple(current_frequency),
                                                      clb.MIN_FREQUENCY, clb.MAX_FREQUENCY,
                                                      QtWidgets.QLabel("Частота, Гц", self))
        edit_frequency_dialog.set_main_widget(edit_frequency_widget)

        edit_frequency_dialog.ui.main_widget_layout.addWidget(edit_frequency_widget)
        edit_frequency_dialog.accepted.connect(self.frequency_editing_finished)
        edit_frequency_dialog.exec()

    def frequency_editing_finished(self):
        # noinspection PyUnresolvedReferences
        edit_widget: EditedListOnlyNumbers = self.sender().get_main_widget()
        frequency_list = edit_widget.get_list()
        self.edit.setText(";".join(utils.float_to_string(f) for f in frequency_list))

    def get_frequency_text(self):
        return self.edit.text()


class ScaleLimitsDialog(QtWidgets.QDialog):
    class Column(IntEnum):
        LIMIT = 0
        CLASS = 1
        SIGNAL_TYPE = 2
        FREQUENCY = 3
        ID = 4

    def __init__(self, a_limits: List[Scale.Limit], a_parent=None):
        super().__init__(a_parent)

        self.ui = ScaleLimitsForm()
        self.ui.setupUi(self)
        self.ui.limits_table.hideColumn(ScaleLimitsDialog.Column.ID)
        self.ui.default_button.hide()

        assert a_limits, "Every scale must have at least 1 limit !!!"

        self.limits = a_limits
        self.deleted_ids = []

        self.ui.limits_table.setItemDelegateForColumn(ScaleLimitsDialog.Column.LIMIT,
                                                      NonOverlappingDoubleClick(self.ui.limits_table))
        self.ui.limits_table.itemChanged.connect(self.set_value_to_user)

        self.ui.add_limit_button.clicked.connect(self.add_limit)
        self.ui.remove_limit_button.clicked.connect(self.remove_limit)

        self.recover_params(self.limits)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.reject_button.clicked.connect(self.reject)

    def __del__(self):
        print("Scale Limits deleted")

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
            self.add_limit_to_table(limit)

    def signal_type_changed(self, a_idx):
        try:
            sender_table_row = self.ui.limits_table.currentRow()
            row_limit_item = self.ui.limits_table.item(sender_table_row, ScaleLimitsDialog.Column.LIMIT)

            value_f = utils.parse_input(row_limit_item.text())
            signal_type = clb.SignalType(a_idx)
            units = clb.signal_type_to_units[signal_type]

            value_str = utils.value_to_user_with_units(units)(value_f)
            row_limit_item.setText(value_str)
        except Exception as err:
            utils.exception_handler(err)

    def extract_params(self) -> List[Scale.Limit]:
        try:
            scales = []
            for row_idx in range(self.ui.limits_table.rowCount()):
                limit = utils.parse_input(self.ui.limits_table.item(row_idx, ScaleLimitsDialog.Column.LIMIT).text())
                device_class = self.ui.limits_table.cellWidget(row_idx, ScaleLimitsDialog.Column.CLASS).value()
                signal_type = \
                    self.ui.limits_table.cellWidget(row_idx, ScaleLimitsDialog.Column.SIGNAL_TYPE).currentIndex()
                frequency = \
                    self.ui.limits_table.cellWidget(row_idx, ScaleLimitsDialog.Column.FREQUENCY).get_frequency_text()
                limit_id = int(self.ui.limits_table.item(row_idx, ScaleLimitsDialog.Column.ID).text())

                scales.append(Scale.Limit(a_id=limit_id, a_limit=limit, a_device_class=device_class,
                                          a_signal_type=clb.SignalType(signal_type), a_frequency=frequency))
            return scales
        except Exception as err:
            utils.exception_handler(err)

    def add_limit_to_table(self, a_limit: Scale.Limit):
        row_idx = self.ui.limits_table.rowCount()
        self.ui.limits_table.insertRow(row_idx)

        class_spinbox = QtWidgets.QDoubleSpinBox(self)
        class_spinbox.setDecimals(4)
        class_spinbox.setMinimum(0.001)
        class_spinbox.setMaximum(10)
        class_spinbox.setSingleStep(0.05)
        class_spinbox.setValue(a_limit.device_class)
        self.ui.limits_table.setCellWidget(row_idx, ScaleLimitsDialog.Column.CLASS, class_spinbox)

        signal_type_combobox = QtWidgets.QComboBox(self)
        for s_t in clb.SignalType:
            signal_type_combobox.addItem(clb.enum_to_signal_type_short[s_t])
        signal_type_combobox.setCurrentIndex(a_limit.signal_type)
        signal_type_combobox.currentIndexChanged.connect(self.signal_type_changed)
        self.ui.limits_table.setCellWidget(row_idx, ScaleLimitsDialog.Column.SIGNAL_TYPE, signal_type_combobox)

        # Обязательно добалять после добавления комбобокса !!!
        self.ui.limits_table.setItem(row_idx, ScaleLimitsDialog.Column.LIMIT,
                                     QtWidgets.QTableWidgetItem(str(a_limit.limit)))

        self.ui.limits_table.setCellWidget(row_idx, ScaleLimitsDialog.Column.FREQUENCY,
                                           FrequencyWidget(self, a_limit.frequency))

        self.ui.limits_table.setItem(row_idx, ScaleLimitsDialog.Column.ID, QtWidgets.QTableWidgetItem(str(a_limit.id)))

    def add_limit(self):
        self.add_limit_to_table(Scale.Limit())

    def remove_limit(self):
        if self.ui.limits_table.rowCount() > 1:
            rows = self.ui.limits_table.selectionModel().selectedRows()
            if rows:
                for idx_model in reversed(rows):
                    print("deleted", idx_model.row())
                    deleted_row = idx_model.row()
                    deleted_id = int(self.ui.limits_table.item(deleted_row, ScaleLimitsDialog.Column.ID).text())
                    self.ui.limits_table.removeRow(deleted_row)
                    # Пределов с id == 0 и так нет в БД
                    if deleted_id != 0:
                        self.deleted_ids.append(deleted_id)

    def exec_and_get_limits(self):
        if self.exec() == QtWidgets.QDialog.Accepted:
            return self.extract_params(), self.deleted_ids
        else:
            return None, None
