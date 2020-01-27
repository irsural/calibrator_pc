from typing import List
import enum

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets, QtCore

from ui.py.new_no_template_measure_form import Ui_Dialog as NewMeasureForm
from custom_widgets.EditListDialog import EditedListOnlyNumbers
import calibrator_constants as clb
import clb_dll
import utils
import qt_utils


class NoTemplateConfig:
    class DisplayResolution(enum.IntEnum):
        XXX = 0
        XX = 1
        X = 2
        X_0 = 3
        X_00 = 4
        X_000 = 5
        X_0000 = 6
        X_00000 = 7

    class StartPoint(enum.IntEnum):
        LOWER = 0
        UPPER = 1

    def __init__(self):
        self.signal_type = clb.SignalType.ACI
        self.clb_name = ""
        self.lower_bound = 0.
        self.upper_bound = 1.
        self.display_resolution = self.DisplayResolution.X
        self.point_approach_accuracy = 10.

        self.auto_calc_points = False
        self.points_step = 0.
        self.start_point_side = self.StartPoint.LOWER

    def __str__(self):
        return f"Signal type: {self.signal_type.name}\n" \
            f"Clb name: {self.clb_name}\n" \
            f"Lower: {self.lower_bound}\n" \
            f"Upper: {self.upper_bound}\n" \
            f"Resolution: {self.display_resolution}\n" \
            f"Accuracy: {self.point_approach_accuracy}\n" \
            f"Auto calc: {self.auto_calc_points}\n" \
            f"Step: {self.points_step}\n" \
            f"Side: {self.start_point_side.name}\n"


class NewNoTemplateMeasureDialog(QDialog):
    config_ready = pyqtSignal(NoTemplateConfig)

    class InputStatus(enum.IntEnum):
        ok = 0
        no_calibrator = 1
        upper_less_than_lower = 2
        upper_less_than_zero = 3
        step_is_zero = 4
        empty_fields = 5
        current_too_big = 6
        voltage_too_big = 7
        bad_input = 8

    input_status_to_msg = {
        InputStatus.ok: "Ввод корректен",
        InputStatus.no_calibrator: "Калибратор не выбран",
        InputStatus.upper_less_than_lower: "Значение верхней точки должно быть больше значения нижней точки",
        InputStatus.upper_less_than_zero: "В режиме переменного тока напряжение/сила тока должны быть положительными",
        InputStatus.step_is_zero: "Шаг поверки не должен быть равен нулю",
        InputStatus.empty_fields: "Необходимо заполнить все поля",
        InputStatus.current_too_big: f"Значение тока не должно превышать |{clb.MAX_CURRENT}| А",
        InputStatus.voltage_too_big: f"Значение напряжения не должно превышать |{clb.MAX_VOLTAGE}| В",
        InputStatus.bad_input: f"Некорректный ввод. Необходимо исправить поля, отмеченные красным цветом"
    }

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config=None, a_parent=None):
        super().__init__(a_parent)

        self.ui = NewMeasureForm()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.measure_config = a_measure_config if a_measure_config is not None else NoTemplateConfig()
        self.value_to_user = utils.value_to_user_with_units("А")

        self.connect_signals()
        self.restore_config()

        self.normalize_edit_value(self.ui.upper_bound_edit)
        self.normalize_edit_value(self.ui.lower_bound_edit)
        self.normalize_edit_value(self.ui.step_edit)

        self.calibrator = a_calibrator

        self.window_existing_timer = QtCore.QTimer()
        self.window_existing_timer.timeout.connect(self.window_existing_chech)
        self.window_existing_timer.start(3000)

    def window_existing_chech(self):
        print("New measure dialog")

    def connect_signals(self):
        self.ui.aci_radio.clicked.connect(self.set_mode_aci)
        self.ui.dci_radio.clicked.connect(self.set_mode_dci)
        self.ui.acv_radio.clicked.connect(self.set_mode_acv)
        self.ui.dcv_radio.clicked.connect(self.set_mode_dcv)

        self.ui.step_help_button.clicked.connect(self.show_step_help)
        self.ui.edit_frequency_button.clicked.connect(self.show_frequency_list)
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)

        self.ui.lower_bound_edit.textEdited.connect(self.edit_text_edited)
        self.ui.lower_bound_edit.editingFinished.connect(self.editinig_finished)
        self.ui.lower_bound_edit.editingFinished.connect(self.ui.lower_bound_edit.clearFocus)

        self.ui.upper_bound_edit.textEdited.connect(self.edit_text_edited)
        self.ui.upper_bound_edit.editingFinished.connect(self.editinig_finished)
        self.ui.upper_bound_edit.editingFinished.connect(self.ui.upper_bound_edit.clearFocus)

        self.ui.step_edit.textEdited.connect(self.edit_text_edited)
        self.ui.step_edit.editingFinished.connect(self.editinig_finished)
        self.ui.step_edit.editingFinished.connect(self.ui.step_edit.clearFocus)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.cancel_button.clicked.connect(self.reject)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        self.ui.clb_list_combobox.clear()
        for clb_name in a_clb_list:
            self.ui.clb_list_combobox.addItem(clb_name)

    @pyqtSlot(clb.State)
    def update_clb_status(self, a_status: clb.State):
        # self.ui.usb_state_label.setText(a_status)
        pass

    def connect_to_clb(self, a_clb_name):
        self.calibrator.connect(a_clb_name)

    def edit_text_edited(self):
        try:
            edit: QtWidgets.QLineEdit = self.sender()
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
            edit: QtWidgets.QLineEdit = self.sender()
            assert isinstance(edit, QtWidgets.QLineEdit), "editinig_finished must be connected to QLineEdit event!"
            self.normalize_edit_value(edit)
        except AssertionError as err:
            print(err)

    def normalize_edit_value(self, edit: QtWidgets.QLineEdit):
        try:
            value = utils.parse_input(edit.text())
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
        signal_type_to_radio[self.measure_config.signal_type].click()

        self.ui.lower_bound_edit.setText(str(self.measure_config.lower_bound))
        self.ui.upper_bound_edit.setText(str(self.measure_config.upper_bound))
        self.ui.step_edit.setText(str(self.measure_config.points_step))
        self.ui.accuracy_spinbox.setValue(self.measure_config.point_approach_accuracy)

        self.ui.display_resolution_combobox.setCurrentIndex(self.measure_config.display_resolution)

        start_point_upper_chosen = self.measure_config.start_point_side == NoTemplateConfig.StartPoint.UPPER
        self.ui.start_point_up_radio.setChecked(start_point_upper_chosen)

        self.ui.auto_calc_points_checkbox.setChecked(self.measure_config.auto_calc_points)

    def save_config(self):
        try:
            self.measure_config.clb_name = self.ui.clb_list_combobox.currentText()
            self.measure_config.lower_bound = utils.parse_input(self.ui.lower_bound_edit.text())
            self.measure_config.upper_bound = utils.parse_input(self.ui.upper_bound_edit.text())
            self.measure_config.display_resolution = self.ui.display_resolution_combobox.currentIndex()
            self.measure_config.point_approach_accuracy = self.ui.accuracy_spinbox.value()

            self.measure_config.auto_calc_points = bool(self.ui.auto_calc_points_checkbox.isChecked())
            self.measure_config.points_step = utils.parse_input(self.ui.step_edit.text())

            self.measure_config.start_point_side = NoTemplateConfig.StartPoint.UPPER if \
                self.ui.start_point_up_radio.isChecked() else NoTemplateConfig.StartPoint.LOWER
            return True
        except ValueError:
            return False

    @pyqtSlot()
    def set_mode_aci(self):
        self.measure_config.signal_type = clb.SignalType.ACI
        self.set_units("А")

    @pyqtSlot()
    def set_mode_dci(self):
        self.measure_config.signal_type = clb.SignalType.DCI
        self.set_units("А")

    @pyqtSlot()
    def set_mode_acv(self):
        self.measure_config.signal_type = clb.SignalType.ACV
        self.set_units("В")

    @pyqtSlot()
    def set_mode_dcv(self):
        self.measure_config.signal_type = clb.SignalType.DCV
        self.set_units("В")

    @pyqtSlot()
    def accept(self):
        if not self.save_config():
            input_status = self.InputStatus.bad_input
        else:
            input_status = self.check_input(self.measure_config)

        if input_status == self.InputStatus.ok:
            self.config_ready.emit(self.measure_config)
            self.done(QDialog.Accepted)
        else:
            QMessageBox.critical(self, "Ошибка ввода", self.input_status_to_msg[input_status], QMessageBox.Ok)

    def check_input(self, a_config: NoTemplateConfig):
        if a_config.clb_name == "":
            return self.InputStatus.no_calibrator
        elif a_config.upper_bound <= a_config.lower_bound:
            return self.InputStatus.upper_less_than_lower
        elif (a_config.signal_type == clb.SignalType.ACI or a_config.signal_type == clb.SignalType.ACV) and \
                (a_config.upper_bound < 0 or a_config.lower_bound < 0):
            return self.InputStatus.upper_less_than_zero
        elif (a_config.signal_type == clb.SignalType.ACI or a_config.signal_type == clb.SignalType.DCI) and \
                (abs(a_config.upper_bound) > clb.MAX_CURRENT or abs(a_config.lower_bound) > clb.MAX_CURRENT):
            return self.InputStatus.current_too_big
        elif (a_config.signal_type == clb.SignalType.ACV or a_config.signal_type == clb.SignalType.DCV) and \
                (abs(a_config.upper_bound) > clb.MAX_VOLTAGE or abs(a_config.lower_bound) > clb.MAX_VOLTAGE):
            return self.InputStatus.voltage_too_big
        elif a_config.auto_calc_points and a_config.points_step == 0:
            return self.InputStatus.step_is_zero
        else:
            return self.InputStatus.ok

    @pyqtSlot()
    def show_frequency_list(self):
        frequency_text = self.ui.frequency_edit.text()
        current_frequency = frequency_text.split(';') if frequency_text else []
        edit_frequency_dialog = EditedListOnlyNumbers(self, tuple(current_frequency),
                                                      "Редактирование частот поверки", "Частота, Гц")
        edit_frequency_dialog.list_ready.connect(self.frequency_editing_finished)
        edit_frequency_dialog.exec()

    @pyqtSlot(list)
    def frequency_editing_finished(self, a_frequency_list: List[str]):
        self.ui.frequency_edit.setText(";".join(a_frequency_list))

    @pyqtSlot()
    def show_step_help(self):
        QMessageBox.information(self, "Ввод шага", "Параметры \"Снизу\" и \"Сверху\" определяют начальную точку,\n"
                                                   "от которой будут рассчитываться точки с интервалом \"Шаг\n"
                                                   "поверки\" (верхняя граница, либо нижняя граница)", QMessageBox.Ok)

    def set_units(self, a_units_str: str):
        self.value_to_user = utils.value_to_user_with_units(a_units_str)
        self.normalize_edit_value(self.ui.upper_bound_edit)
        self.normalize_edit_value(self.ui.lower_bound_edit)
        self.normalize_edit_value(self.ui.step_edit)
