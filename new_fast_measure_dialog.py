from typing import List
import enum

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets, QtCore, QtGui

from ui.py.new_fast_measure_form import Ui_Dialog as NewFastMeasureForm
from custom_widgets.EditListDialog import EditedListOnlyNumbers, OkCancelDialog
import calibrator_constants as clb
import utils
import qt_utils


class FastMeasureParams:
    class StartPoint(enum.IntEnum):
        LOWER = 0
        UPPER = 1

    def __init__(self):
        self.signal_type = clb.SignalType.ACV
        self.accuracy_class = 2.5
        self.upper_bound = 10.
        self.minimal_discrete = 1.
        self.comment = ""

        self.date = QtCore.QDate.currentDate().toString("dd.MM.yyyy")
        self.time = QtCore.QTime.currentTime().toString("H:mm")

        self.auto_calc_points = True
        self.lower_bound = 0.
        self.points_step = 2.
        self.start_point_side = self.StartPoint.LOWER
        self.amplitudes = []
        self.frequency = ["40", "50", "60"]

    def __str__(self):
        return f"Signal type: {self.signal_type.name}\n" \
            f"Lower: {self.lower_bound}\n" \
            f"Upper: {self.upper_bound}\n" \
            f"Discrete: {self.minimal_discrete}\n" \
            f"Class: {self.accuracy_class}\n" \
            f"Auto calc: {self.auto_calc_points}\n" \
            f"Step: {self.points_step}\n" \
            f"Side: {self.start_point_side.name}\n" \
            f"Frequency: {self.frequency}\n"


class NewFastMeasureDialog(QDialog):
    config_ready = pyqtSignal(FastMeasureParams)

    class InputStatus(enum.IntEnum):
        ok = 0
        upper_less_than_lower = 1
        upper_less_than_zero = 2
        step_is_zero = 3
        empty_fields = 4
        current_too_big = 5
        voltage_too_big = 6
        bad_input = 7
        zero_minimal_discrete = 8
        no_frequency = 9

    input_status_to_msg = {
        InputStatus.ok: "Ввод корректен",
        InputStatus.upper_less_than_lower: "Значение верхней точки должно быть больше значения нижней точки",
        InputStatus.upper_less_than_zero: "В режиме переменного тока напряжение/сила тока должны быть положительными",
        InputStatus.step_is_zero: "Шаг поверки не должен быть равен нулю",
        InputStatus.empty_fields: "Необходимо заполнить все поля",
        InputStatus.current_too_big: f"Значение тока не должно превышать |{clb.MAX_CURRENT}| А",
        InputStatus.voltage_too_big: f"Значение напряжения не должно превышать |{clb.MAX_VOLTAGE}| В",
        InputStatus.bad_input: f"Некорректный ввод. Необходимо исправить поля, отмеченные красным цветом",
        InputStatus.zero_minimal_discrete: f"Минимальный дискрет не должен быть равен нулю",
        InputStatus.no_frequency: "Значения частоты не заданы"
    }

    def __init__(self, a_fast_params=None, a_parent=None):
        super().__init__(a_parent)

        self.ui = NewFastMeasureForm()
        self.ui.setupUi(self)
        self.ui.invisible_default_button.hide()
        self.setFixedSize(self.width(), self.height())

        self.fast_params = a_fast_params if a_fast_params is not None else FastMeasureParams()
        self.value_to_user = utils.value_to_user_with_units("А")

        self.connect_signals()
        self.restore_config()

        self.normalize_edit_value(self.ui.upper_bound_edit)
        self.normalize_edit_value(self.ui.lower_bound_edit)
        self.normalize_edit_value(self.ui.step_edit)

        self.edit_frequency_widget: EditedListOnlyNumbers = None

    # noinspection DuplicatedCode
    def connect_signals(self):
        self.ui.aci_radio.clicked.connect(self.set_mode_aci)
        self.ui.dci_radio.clicked.connect(self.set_mode_dci)
        self.ui.acv_radio.clicked.connect(self.set_mode_acv)
        self.ui.dcv_radio.clicked.connect(self.set_mode_dcv)

        self.ui.edit_frequency_button.clicked.connect(self.show_frequency_list)

        self.ui.lower_bound_edit.textEdited.connect(self.edit_text_edited)
        self.ui.lower_bound_edit.editingFinished.connect(self.editinig_finished)

        self.ui.upper_bound_edit.textEdited.connect(self.edit_text_edited)
        self.ui.upper_bound_edit.editingFinished.connect(self.editinig_finished)

        self.ui.step_edit.textEdited.connect(self.edit_text_edited)
        self.ui.step_edit.editingFinished.connect(self.editinig_finished)

        self.ui.minimal_discrete.textEdited.connect(self.edit_text_edited)
        self.ui.minimal_discrete.editingFinished.connect(self.editinig_finished)

        self.ui.comment_edit.editingFinished.connect(self.ui.comment_edit.clearFocus)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)

    def edit_text_edited(self):
        try:
            edit: QtCore.QObject = self.sender()
            assert isinstance(edit, QtWidgets.QLineEdit), "edit_text_edited must be connected to QLineEdit event!"

            self.update_edit_color(edit)
        except AssertionError as err:
            print(err)

    @staticmethod
    def update_edit_color(a_edit: QtWidgets.QLineEdit):
        try:
            utils.parse_input(a_edit.text())
            a_edit.setStyleSheet(qt_utils.QSTYLE_COLOR_WHITE)
        except ValueError:
            a_edit.setStyleSheet(qt_utils.QSTYLE_COLOR_RED)

    @pyqtSlot()
    def editinig_finished(self):
        try:
            edit: QtCore.QObject = self.sender()
            assert isinstance(edit, QtWidgets.QLineEdit), "editinig_finished must be connected to QLineEdit event!"
            self.normalize_edit_value(edit)
        except AssertionError as err:
            print(err)

    def normalize_edit_value(self, edit: QtWidgets.QLineEdit):
        try:
            value = utils.parse_input(edit.text())
            value = clb.bound_amplitude(value, self.fast_params.signal_type)
            edit.setText(self.value_to_user(value))
            self.update_edit_color(edit)
        except ValueError:
            pass

    def restore_config(self):
        signal_type_to_radio = {
            clb.SignalType.ACI: self.ui.aci_radio,
            clb.SignalType.ACV: self.ui.acv_radio,
            clb.SignalType.DCI: self.ui.dci_radio,
            clb.SignalType.DCV: self.ui.dcv_radio,
        }
        signal_type_to_radio[self.fast_params.signal_type].click()

        self.ui.upper_bound_edit.setText(self.value_to_user(self.fast_params.upper_bound))
        self.ui.accuracy_class_spinbox.setValue(self.fast_params.accuracy_class)
        self.ui.minimal_discrete.setText(self.value_to_user(self.fast_params.minimal_discrete))
        self.ui.comment_edit.setText(self.fast_params.comment)

        self.ui.auto_calc_points_checkbox.setChecked(self.fast_params.auto_calc_points)
        self.ui.lower_bound_edit.setText(self.value_to_user(self.fast_params.lower_bound))
        self.ui.frequency_edit.setText(";".join(self.fast_params.frequency))
        self.ui.step_edit.setText(self.value_to_user(self.fast_params.points_step))
        start_point_upper_chosen = self.fast_params.start_point_side == FastMeasureParams.StartPoint.UPPER
        self.ui.start_point_up_radio.setChecked(start_point_upper_chosen)

    def save_config(self):
        try:
            self.fast_params.upper_bound = utils.parse_input(self.ui.upper_bound_edit.text())
            self.fast_params.accuracy_class = self.ui.accuracy_class_spinbox.value()
            self.fast_params.minimal_discrete = utils.parse_input(self.ui.minimal_discrete.text())
            self.fast_params.comment = self.ui.comment_edit.text()

            self.fast_params.auto_calc_points = bool(self.ui.auto_calc_points_checkbox.isChecked())
            self.fast_params.lower_bound = utils.parse_input(self.ui.lower_bound_edit.text())
            self.fast_params.points_step = utils.parse_input(self.ui.step_edit.text())

            self.fast_params.frequency = ["0"] if clb.is_dc_signal[self.fast_params.signal_type] else \
                self.ui.frequency_edit.text().split(';')

            self.fast_params.start_point_side = FastMeasureParams.StartPoint.UPPER if \
                self.ui.start_point_up_radio.isChecked() else FastMeasureParams.StartPoint.LOWER
            return True
        except ValueError:
            return False

    @pyqtSlot()
    def set_mode_aci(self):
        self.fast_params.signal_type = clb.SignalType.ACI
        self.set_units("А")

    @pyqtSlot()
    def set_mode_dci(self):
        self.fast_params.signal_type = clb.SignalType.DCI
        self.set_units("А")

    @pyqtSlot()
    def set_mode_acv(self):
        self.fast_params.signal_type = clb.SignalType.ACV
        self.set_units("В")

    @pyqtSlot()
    def set_mode_dcv(self):
        self.fast_params.signal_type = clb.SignalType.DCV
        self.set_units("В")

    @pyqtSlot()
    def accept(self):
        if not self.save_config():
            input_status = self.InputStatus.bad_input
        else:
            input_status = self.check_input(self.fast_params)
        print(self.fast_params.frequency)
        if input_status == self.InputStatus.ok:
            self.fast_params.amplitudes = [] if not self.fast_params.auto_calc_points else self.calc_points()
            if self.fast_params.frequency[0] == "":
                self.fast_params.frequency = ["0"]

            self.config_ready.emit(self.fast_params)
            self.done(QDialog.Accepted)
        else:
            QMessageBox.critical(self, "Ошибка ввода", self.input_status_to_msg[input_status], QMessageBox.Ok)

    def check_input(self, a_config: FastMeasureParams):
        if a_config.minimal_discrete == 0:
            return self.InputStatus.zero_minimal_discrete
        elif a_config.upper_bound <= a_config.lower_bound:
            return self.InputStatus.upper_less_than_lower
        elif clb.is_ac_signal[a_config.signal_type] and (a_config.upper_bound < 0 or a_config.lower_bound < 0):
            return self.InputStatus.upper_less_than_zero
        elif not clb.is_voltage_signal[a_config.signal_type] and \
                (abs(a_config.upper_bound) > clb.MAX_CURRENT or abs(a_config.lower_bound) > clb.MAX_CURRENT):
            return self.InputStatus.current_too_big
        elif clb.is_voltage_signal[a_config.signal_type] and \
                (abs(a_config.upper_bound) > clb.MAX_VOLTAGE or abs(a_config.lower_bound) > clb.MAX_VOLTAGE):
            return self.InputStatus.voltage_too_big
        elif a_config.auto_calc_points and a_config.points_step == 0:
            return self.InputStatus.step_is_zero
        elif clb.is_ac_signal[a_config.signal_type] and not a_config.frequency:
            return self.InputStatus.no_frequency
        else:
            return self.InputStatus.ok

    @pyqtSlot()
    def show_frequency_list(self):
        frequency_text = self.ui.frequency_edit.text()
        current_frequency = frequency_text.split(';') if frequency_text else []
        edit_frequency_dialog = OkCancelDialog(self, "Редактирование частот поверки")

        self.edit_frequency_widget = EditedListOnlyNumbers(edit_frequency_dialog, tuple(current_frequency),
                                                           "Частота, Гц")

        edit_frequency_dialog.ui.main_widget_layout.addWidget(self.edit_frequency_widget)
        edit_frequency_dialog.accepted.connect(self.frequency_editing_finished)
        edit_frequency_dialog.exec()

    @pyqtSlot()
    def frequency_editing_finished(self):
        frequency_list = self.edit_frequency_widget.get_list()
        self.ui.frequency_edit.setText(";".join(frequency_list))

    def set_units(self, a_units_str: str):
        self.value_to_user = utils.value_to_user_with_units(a_units_str)
        self.normalize_edit_value(self.ui.upper_bound_edit)
        self.normalize_edit_value(self.ui.lower_bound_edit)
        self.normalize_edit_value(self.ui.step_edit)
        self.normalize_edit_value(self.ui.minimal_discrete)

    def calc_points(self):
        lower_point, upper_point = (self.fast_params.lower_bound, self.fast_params.upper_bound) if \
            self.fast_params.StartPoint == FastMeasureParams.StartPoint.LOWER else \
            (self.fast_params.upper_bound, self.fast_params.lower_bound)

        return utils.auto_calc_points(lower_point, upper_point, self.fast_params.points_step)
