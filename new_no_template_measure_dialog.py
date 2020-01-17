from ui.py.new_no_template_measure_form import Ui_Dialog as NewMeasureForm
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import calibrator_constants as clb
import clb_dll
import enum
import utils


class NoTemplateConfig:
    class DisplayResolution(enum.IntEnum):
        XXX = 0
        XX = 1
        X = 2
        X_0 = 3
        X_00 = 4
        X_000 = 5

    class StartPoint(enum.IntEnum):
        LOWER = 0
        UPPER = 1

    def __init__(self):
        self.signal_type = clb.SignalType.ACI
        self.clb_name = ""
        self.lower_bound = 0.
        self.upper_bound = 0.
        self.display_resolution = self.DisplayResolution.X
        self.point_approach_accuracy = 10.

        self.auto_calc_points = False
        self.points_step = 0.
        self.start_point = self.StartPoint.UPPER

    def __str__(self):
        return f"Signal type: {self.signal_type.name}\n" \
            f"Clb name: {self.clb_name}\n" \
            f"Lower: {self.lower_bound}\n" \
            f"Upper: {self.upper_bound}\n" \
            f"Resolution: {self.display_resolution}\n" \
            f"Accuracy: {self.point_approach_accuracy}\n" \
            f"Auto calc: {self.auto_calc_points}\n" \
            f"Step: {self.points_step}\n" \
            f"Side: {self.start_point.name}\n"


class NewNoTemplateMeasureDialog(QDialog):
    window_is_closed = pyqtSignal()

    class InputStatus(enum.IntEnum):
        ok = 0
        no_calibrator = 1
        upper_less_than_lower = 2
        upper_less_than_zero = 3
        step_is_zero = 4
        empty_fields = 5
        current_too_big = 6
        voltage_too_big = 7

    input_status_to_msg = {
        InputStatus.ok: "Ввод корректен",
        InputStatus.no_calibrator: "Калибратор не выбран",
        InputStatus.upper_less_than_lower: "Значение верхней точки должно быть больше значения нижней точки",
        InputStatus.upper_less_than_zero: "В режиме переменного тока напряжение/сила тока должны быть положительными",
        InputStatus.step_is_zero: "Шаг поверки не должен быть равен нулю",
        InputStatus.empty_fields: "Необходимо заполнить все поля",
        InputStatus.current_too_big: f"Значение тока не должно превышать |{clb.MAX_CURRENT}| А",
        InputStatus.voltage_too_big: f"Значение напряжения не должно превышать |{clb.MAX_VOLTAGE}| В",
    }

    def __init__(self, a_calibrator: clb_dll.ClbDrv):
        super().__init__()

        self.ui = NewMeasureForm()
        self.ui.setupUi(self)
        self.show()

        self.measure_config = NoTemplateConfig()

        self.calibrator = a_calibrator

        self.ui.aci_radio.clicked.connect(self.set_mode_aci)
        self.ui.dci_radio.clicked.connect(self.set_mode_dci)
        self.ui.acv_radio.clicked.connect(self.set_mode_acv)
        self.ui.dcv_radio.clicked.connect(self.set_mode_dcv)

        self.ui.step_help_button.clicked.connect(self.show_step_help)

        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        self.ui.clb_list_combobox.clear()
        for clb_name in a_clb_list:
            self.ui.clb_list_combobox.addItem(clb_name)

    @pyqtSlot(str)
    def update_clb_status(self, a_status: str):
        # self.ui.usb_state_label.setText(a_status)
        pass

    def connect_to_clb(self, a_clb_name):
        self.calibrator.connect(a_clb_name)

    def restore_config(self, a_measure_config: NoTemplateConfig):
        # self.measure_config = a_measure_config
        pass

    def save_config(self):
        self.measure_config.clb_name = self.ui.clb_list_combobox.currentText()
        self.measure_config.lower_bound = utils.parse_input(self.ui.lower_bound_edit.text())
        self.measure_config.upper_bound = utils.parse_input(self.ui.upper_bound_edit.text())
        self.measure_config.display_resolution = self.ui.display_resolution_combobox.currentIndex()
        self.measure_config.point_approach_accuracy = self.ui.accuracy_spinbox.value()

        self.measure_config.auto_calc_points = bool(self.ui.auto_calc_points_checkbox.isChecked())
        self.measure_config.points_step = utils.parse_input(self.ui.step_edit.text())
        self.measure_config.start_point = NoTemplateConfig.StartPoint.UPPER if self.ui.approach_up_radio.isChecked() \
            else NoTemplateConfig.StartPoint.LOWER

    def get_config(self):
        return self.measure_config

    @pyqtSlot()
    def set_mode_aci(self):
        self.measure_config.signal_type = clb.SignalType.ACI
        self.set_units_wildcard("А")

    @pyqtSlot()
    def set_mode_dci(self):
        self.measure_config.signal_type = clb.SignalType.DCI
        self.set_units_wildcard("А")

    @pyqtSlot()
    def set_mode_acv(self):
        self.measure_config.signal_type = clb.SignalType.ACV
        self.set_units_wildcard("В")

    @pyqtSlot()
    def set_mode_dcv(self):
        self.measure_config.signal_type = clb.SignalType.DCV
        self.set_units_wildcard("В")

    def set_units_wildcard(self, a_wildcard_text):
        self.ui.units_wildcard_1.setText(a_wildcard_text)
        self.ui.units_wildcard_2.setText(a_wildcard_text)
        self.ui.units_wildcard_3.setText(a_wildcard_text)

    @pyqtSlot()
    def accept(self):
        self.save_config()

        input_status = self.check_input(self.measure_config)
        if input_status == self.InputStatus.ok:
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
    def show_step_help(self):
        QMessageBox.information(self, "Ввод шага", "Параметры \"Снизу\" и \"Сверху\" определяют начальную точку,\n"
                                                   "от которой будут рассчитываться точки с интервалом \"Шаг\n"
                                                   "поверки\" (верхняя граница, либо нижняя граница)", QMessageBox.Ok)


