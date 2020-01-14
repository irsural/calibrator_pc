from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer

from new_no_template_measure_dialog import NoTemplateConfig
from ui.py.no_template_mode_form import Ui_Form as NoTemplateForm
import clb_dll, utils
import calibrator_constants as clb


class NoTemplateWindow(QWidget):
    window_is_closed = pyqtSignal()

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: NoTemplateConfig):
        super().__init__()

        self.ui = NoTemplateForm()
        self.ui.setupUi(self)

        self.calibrator = a_calibrator
        self.measure_config = a_measure_config
        self.units_text = "А" if self.measure_config == clb.SignalType.ACI or \
            self.measure_config == clb.SignalType.DCI else "В"

        self.setWindowTitle(f"{self.measure_config.clb_name}. Измерение без шаблона. "
                            f"{clb.enum_to_signal_type[self.measure_config.signal_type]}. "
                            f"{self.measure_config.upper_bound} {self.units_text}")
        self.calibrator.connect(self.measure_config.clb_name)

        self.connect_signals()
        self.started = False

        self.clb_check_timer = QTimer()
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)
        self.block_signals = False

    def connect_signals(self):
        self.ui.start_stop_button.clicked.connect(self.start_stop_measure)
        self.ui.amplitude_edit.textChanged.connect(self.amplitude_edit_text_changed)

    def amplitude_edit_text_changed(self):
        if not self.block_signals:
            utils.update_edit_color(self.calibrator.amplitude, self.ui.amplitude_edit)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        pass

    @pyqtSlot(str)
    def update_clb_status(self, a_status: str):
        self.ui.usb_state_label.setText(a_status)

    def sync_clb_parameters(self):
        try:
            self.block_signals = True

            if self.calibrator.amplitude_changed():
                self.ui.amplitude_edit.setText(f"{self.calibrator.amplitude:.9f}")

            if self.calibrator.frequency_changed():
                self.ui.frequency_edit.setText(f"{self.calibrator.frequency:.9f}")

            if self.calibrator.signal_enable_changed():
                if self.calibrator.signal_enable:
                    self.ui.clb_state_label.setText("Включен")
                else:
                    self.ui.clb_state_label.setText("Отключен")

            if self.calibrator.signal_type_changed():
                if self.calibrator.signal_type != self.measure_config.signal_type:
                    self.calibrator.signal_type = self.measure_config.signal_type

            self.block_signals = False
        except Exception as err:
            print(err)

    @pyqtSlot()
    def start_stop_measure(self):
        try:
            if not self.started:
                reply = QMessageBox.question(self, "Подтвердите действие",
                                             f"Начать поверку?\n"
                                             f"На калибраторе будет включен сигнал и установлены следующие параметры:\n"
                                             f"Режим измерения: Фиксированный диапазон\n"
                                             f"Тип сигнала: {clb.enum_to_signal_type[self.measure_config.signal_type]}\n"
                                             f"Амплитуда: {self.measure_config.upper_bound} {self.units_text}",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    self.start_measure()
            else:
                self.close()
        except Exception as err:
            print(err)

    def start_measure(self):
        self.ui.start_stop_button.setText("Закончить\nповерку")
        self.started = True

        self.calibrator.mode = clb.Mode.FIXED_RANGE
        self.calibrator.amplitude = self.measure_config.upper_bound
        self.calibrator.signal_type = self.measure_config.signal_type
        self.calibrator.signal_enable = True

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.calibrator.signal_enable = False
            self.hide()
            self.window_is_closed.emit()
        else:
            event.ignore()

