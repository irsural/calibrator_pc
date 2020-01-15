from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QItemSelectionModel, QPoint, QModelIndex, Qt
from PyQt5.QtGui import QWheelEvent

from new_no_template_measure_dialog import NoTemplateConfig
from ui.py.no_template_mode_form import Ui_Form as NoTemplateForm
import clb_dll
import utils
import calibrator_constants as clb
from QNoTemplateMeasureModel import PointData, QNoTemplateMeasureModel


class NoTemplateWindow(QWidget):
    window_is_closed = pyqtSignal()
    remove_points = pyqtSignal(list)

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: NoTemplateConfig):
        super().__init__()

        self.ui = NoTemplateForm()
        self.ui.setupUi(self)

        self.measure_model = QNoTemplateMeasureModel(self)
        self.ui.measure_table.setModel(self.measure_model)

        self.measure_config = a_measure_config
        self.units_text = "А"
        self.set_window_elements()

        self.calibrator = a_calibrator
        self.calibrator.connect(self.measure_config.clb_name)
        # Нужно для автоматического определения стороны подхода к точке
        self.current_point = PointData()
        self.prev_amplitude = 0

        self.connect_signals()
        self.started = False

        self.clb_check_timer = QTimer()
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)
        # self.block_signals = False

    def set_window_elements(self):
        self.units_text = "А" if self.measure_config == clb.SignalType.ACI or \
                                 self.measure_config == clb.SignalType.DCI else "В"

        self.setWindowTitle(f"{self.measure_config.clb_name}. Измерение без шаблона. "
                            f"{clb.enum_to_signal_type[self.measure_config.signal_type]}. "
                            f"{self.measure_config.upper_bound} {self.units_text}")

        if self.measure_config.auto_calc_points:
            if self.measure_config.start_point == NoTemplateConfig.StartPoint.LOWER:
                calculated_points = utils.auto_calc_points(self.measure_config.lower_bound,
                                                           self.measure_config.upper_bound,
                                                           self.measure_config.points_step)
            else:
                calculated_points = utils.auto_calc_points(self.measure_config.upper_bound,
                                                           self.measure_config.lower_bound,
                                                           self.measure_config.points_step)

            for point in calculated_points:
                self.measure_model.appendPoint(PointData(point, 0, PointData.ApproachSize.NONE))

    def connect_signals(self):
        self.ui.start_stop_button.clicked.connect(self.start_stop_measure)
        self.ui.save_point_button.clicked.connect(self.save_point)
        self.ui.delete_point_button.clicked.connect(self.delete_point)
        self.remove_points.connect(self.measure_model.removeSelected)

        self.ui.rough_plus_button.clicked.connect(self.rough_plus_button_clicked)
        self.ui.rough_minus_button.clicked.connect(self.rough_minus_button_clicked)
        self.ui.common_plus_button.clicked.connect(self.common_plus_button_clicked)
        self.ui.common_minus_button.clicked.connect(self.common_minus_button_clicked)
        self.ui.exact_plus_button.clicked.connect(self.exact_plus_button_clicked)
        self.ui.exact_minus_button.clicked.connect(self.exact_minus_button_clicked)
        self.ui.fixed_plus_button.clicked.connect(self.fixed_plus_button_clicked)
        self.ui.fixed_minus_button.clicked.connect(self.fixed_minus_button_clicked)

        self.ui.amplitude_edit.textEdited.connect(self.amplitude_edit_text_changed)
        self.ui.frequency_edit.textEdited.connect(self.frequency_edit_text_changed)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        pass

    @pyqtSlot(str)
    def update_clb_status(self, a_status: str):
        self.ui.usb_state_label.setText(a_status)

    def sync_clb_parameters(self):
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
                print(self.calibrator.signal_type)
                self.calibrator.signal_type = self.measure_config.signal_type

    def wheelEvent(self, event: QWheelEvent):
        try:
            degrees_num = event.angleDelta() / 8
            steps_num: QPoint = degrees_num / 15
            steps: int = steps_num.y()

            keys = event.modifiers()
            if (keys & Qt.ControlModifier) and (keys & Qt.ShiftModifier):
                self.change_amplitude(1 * steps)
            elif keys & Qt.ShiftModifier:
                self.change_amplitude(clb.AmplitudeStep.EXACT * steps)
            elif keys & Qt.ControlModifier:
                self.change_amplitude(clb.AmplitudeStep.ROUGH * steps)
            else:
                self.change_amplitude(clb.AmplitudeStep.COMMON * steps)

            event.accept()
        except Exception as err:
            print(err)

    def set_amplitude(self, a_amplitude):
        self.calibrator.amplitude = a_amplitude
        self.ui.amplitude_edit.setText(f"{self.calibrator.amplitude:.9f}")

    def set_frequency(self, a_frequency):
        self.calibrator.frequency = a_frequency
        self.ui.frequency_edit.setText(f"{self.calibrator.frequency:.9f}")

    def change_amplitude(self, a_step):
        self.set_amplitude(self.calibrator.amplitude + a_step)

    @pyqtSlot()
    def start_stop_measure(self):
        try:
            if not self.started:
                reply = QMessageBox.question(self, "Подтвердите действие",
                                             f"Начать поверку?\n"
                                             f"На калибраторе будет включен сигнал и установлены следующие параметры:\n"
                                             f"Режим измерения: Фиксированный диапазон\n"
                                             f"Тип сигнала: {clb.enum_to_signal_type[self.measure_config.signal_type]}\n"
                                             f"Амплитуда: {self.measure_config.upper_bound} + ???% {self.units_text}",
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
        self.set_amplitude(self.measure_config.upper_bound)
        self.calibrator.signal_type = self.measure_config.signal_type
        self.calibrator.signal_enable = True

    @pyqtSlot()
    def save_point(self):
        try:
            self.measure_model.appendPoint(PointData(self.guess_point(self.calibrator.amplitude),
                                                     self.calibrator.amplitude, PointData.ApproachSize.UP))
        except Exception as err:
            print(err)

    def guess_point(self, a_point_value):
        resolution = self.measure_config.display_resolution
        return a_point_value

    def delete_point(self):
        try:
            rows: list[QModelIndex] = self.ui.measure_table.selectionModel().selectedRows()

            if rows:
                row_indexes = []
                deleted_points = ""
                for index_model in rows:
                    point_str = self.get_table_item_by_index(index_model.row(), QNoTemplateMeasureModel.Column.POINT)
                    deleted_points += f"{point_str}\n"
                    row_indexes.append(index_model.row())

                reply = QMessageBox.question(self, "Подтвердите действие", "Удалить следующие точки?\n\n" +
                                             deleted_points, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.remove_points.emit(row_indexes)

        except Exception as err:
            print(err)

    def get_table_item_by_index(self, a_row: int, a_column: int):
        index = self.ui.measure_table.model().index(a_row, a_column)
        data = self.ui.measure_table.model().data(index)
        return str(data)

    def amplitude_edit_text_changed(self):
        utils.update_edit_color(self.calibrator.amplitude, self.ui.amplitude_edit)

    def frequency_edit_text_changed(self):
        utils.update_edit_color(self.calibrator.frequency, self.ui.frequency_edit)

    @pyqtSlot()
    def rough_plus_button_clicked(self):
        self.change_amplitude(clb.AmplitudeStep.ROUGH)

    @pyqtSlot()
    def rough_minus_button_clicked(self):
        self.change_amplitude(-clb.AmplitudeStep.ROUGH)

    @pyqtSlot()
    def common_plus_button_clicked(self):
        self.change_amplitude(clb.AmplitudeStep.COMMON)

    @pyqtSlot()
    def common_minus_button_clicked(self):
        self.change_amplitude(-clb.AmplitudeStep.COMMON)

    @pyqtSlot()
    def exact_plus_button_clicked(self):
        self.change_amplitude(clb.AmplitudeStep.EXACT)

    @pyqtSlot()
    def exact_minus_button_clicked(self):
        self.change_amplitude(-clb.AmplitudeStep.EXACT)

    @pyqtSlot()
    def fixed_plus_button_clicked(self):
        self.change_amplitude(1)

    @pyqtSlot()
    def fixed_minus_button_clicked(self):
        self.change_amplitude(-1)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("here1")
            self.calibrator.signal_enable = False
            self.hide()
            print("here3")
            self.window_is_closed.emit()
            print("here4")
            event.accept()
        else:
            event.ignore()

