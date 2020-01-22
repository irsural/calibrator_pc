from PyQt5.QtWidgets import QDialog, QMessageBox, QMenu, QAction, QTableView
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QPoint, QModelIndex, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QWheelEvent
from typing import List

from new_no_template_measure_dialog import NoTemplateConfig
from ui.py.no_template_mode_form import Ui_Form as NoTemplateForm
import clb_dll
import utils
import qt_utils
import calibrator_constants as clb
from QNoTemplateMeasureModel import PointData, QNoTemplateMeasureModel


class NoTemplateWindow(QDialog):
    remove_points = pyqtSignal(list)

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: NoTemplateConfig, a_parent=None):
        super().__init__(a_parent)

        self.ui = NoTemplateForm()
        self.ui.setupUi(self)

        self.measure_model = QNoTemplateMeasureModel(self)
        self.ui.measure_table.setModel(self.measure_model)
        self.header_menu, self.manual_connections = self.create_table_header_context_menu(self.ui.measure_table)
        self.current_point = PointData()

        self.measure_config = a_measure_config
        self.units_text = "А"
        self.set_window_elements()
        self.fixed_range_amplitude = 0
        self.highest_amplitude = utils.increase_on_percent(self.measure_config.upper_bound,
                                                           self.measure_config.point_approach_accuracy)

        self.value_to_user = utils.value_to_user_with_units(self.units_text)

        self.fixed_range_amplitudes_list = [0.0001, 0.01, 0.1, 1, 10, 20, 100]
        self.fill_fixed_step_combobox(self.fixed_range_amplitudes_list)

        self.calibrator = a_calibrator
        self.clb_state = clb.State.DISCONNECTED
        self.calibrator.signal_type = self.measure_config.signal_type
        self.set_amplitude(self.calibrator.amplitude)
        self.set_frequency(self.calibrator.frequency)
        self.fixed_step = 1

        self.connect_signals()
        self.started = False

        self.clb_check_timer = QTimer(self)
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)

    def create_table_header_context_menu(self, a_table: QTableView):
        table_header = a_table.horizontalHeader()
        table_header.setContextMenuPolicy(Qt.CustomContextMenu)
        table_header.customContextMenuRequested.connect(self.show_active_table_columns)

        menu = QMenu(self)
        lambda_connections = []
        for column in range(a_table.model().columnCount()):
            header_name = a_table.model().headerData(column, Qt.Horizontal)
            menu_checkbox = QAction(header_name, self)
            menu_checkbox.setCheckable(True)
            if not a_table.isColumnHidden(column):
                menu_checkbox.setChecked(True)
            menu.addAction(menu_checkbox)

            lambda_connections.append((menu_checkbox, menu_checkbox.triggered.connect(
                lambda state, col=column: self.hide_selected_table_column(state, col))))

        return menu, lambda_connections

    def set_window_elements(self):
        self.units_text = "А" if self.measure_config.signal_type == clb.SignalType.ACI or \
                                 self.measure_config.signal_type == clb.SignalType.DCI else "В"

        if self.measure_config.signal_type == clb.SignalType.DCI or \
                self.measure_config.signal_type == clb.SignalType.DCV:
            self.ui.apply_frequency_button.setDisabled(True)
            self.ui.frequency_edit.setDisabled(True)

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
                self.measure_model.appendPoint(PointData(point, 0, 0))

    def fill_fixed_step_combobox(self, a_values: list):
        for val in a_values:
            self.ui.fixed_step_combobox.addItem(self.value_to_user(val))

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
        self.ui.apply_amplitude_button.clicked.connect(self.apply_amplitude_button_clicked)
        self.ui.amplitude_edit.returnPressed.connect(self.apply_amplitude_button_clicked)

        self.ui.frequency_edit.textEdited.connect(self.frequency_edit_text_changed)
        self.ui.apply_frequency_button.clicked.connect(self.apply_frequency_button_clicked)
        self.ui.frequency_edit.returnPressed.connect(self.apply_frequency_button_clicked)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        pass

    @pyqtSlot(clb.State)
    def update_clb_status(self, a_status: clb.State):
        self.clb_state = a_status
        self.ui.clb_state_label.setText(clb.enum_to_state[a_status])

    def sync_clb_parameters(self):
        if self.clb_state != clb.State.DISCONNECTED:
            if self.calibrator.amplitude_changed():
                self.set_amplitude(self.calibrator.amplitude)

            if self.calibrator.frequency_changed():
                self.set_frequency(self.calibrator.frequency)

            # Эта переменная синхронизируется в startwindow.py
            if self.calibrator.signal_enable:
                pass
            else:
                pass

            if self.calibrator.signal_type_changed():
                if self.calibrator.signal_type != self.measure_config.signal_type:
                    self.calibrator.signal_type = self.measure_config.signal_type

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.ui.measure_table.hasFocus():
            key = event.key()
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                rows: List[QModelIndex] = self.ui.measure_table.selectionModel().selectedRows()
                if rows:
                    self.ui.measure_table.edit(rows[0])
        else:
            event.accept()

    def wheelEvent(self, event: QWheelEvent):
        if self.ui.amplitude_edit.underMouse() or self.ui.frequency_edit.underMouse():
            steps = qt_utils.get_wheel_steps(event)
            keys = event.modifiers()
            tune_foo = self.tune_amplitude if self.ui.amplitude_edit.underMouse() else self.tune_frequency

            if (keys & Qt.ControlModifier) and (keys & Qt.ShiftModifier):
                if self.ui.amplitude_edit.underMouse():
                    self.set_amplitude(self.calibrator.amplitude + (self.fixed_step * steps))
            elif keys & Qt.ShiftModifier:
                tune_foo(clb.AmplitudeStep.EXACT * steps)
            elif keys & Qt.ControlModifier:
                tune_foo(clb.AmplitudeStep.ROUGH * steps)
            else:
                tune_foo(clb.AmplitudeStep.COMMON * steps)

        event.accept()

    def set_amplitude(self, a_amplitude: float):
        self.update_current_point(a_amplitude)
        self.calibrator.amplitude = a_amplitude
        self.ui.amplitude_edit.setText(self.value_to_user(self.calibrator.amplitude))

    def set_frequency(self, a_frequency):
        self.calibrator.frequency = a_frequency
        self.ui.frequency_edit.setText(utils.remove_tail_zeroes(f"{self.calibrator.frequency:.9f}"))

    def tune_amplitude(self, a_step):
        try:
            self.set_amplitude(utils.relative_step_change(self.calibrator.amplitude, a_step))
        except ValueError as err:
            # Возникает при скролле с нуля
            print(err)

    def tune_frequency(self, a_step):
        try:
            if self.ui.frequency_edit.isEnabled():
                self.set_frequency(utils.relative_step_change(self.calibrator.frequency, a_step))
        except ValueError as err:
            # Возникает при скролле с нуля
            print(err)

    def update_current_point(self, a_current_value):
        """
        Обновляет данные, которые будут записаны в таблицу по кнопке "Сохранить точку"
        :param a_current_value: Новое значение амплитуды
        """
        self.current_point.point = self.guess_point(a_current_value)
        self.current_point.prev_value = self.current_point.value
        self.current_point.value = a_current_value

    @pyqtSlot()
    def start_stop_measure(self):
        try:
            if not self.started:
                reply = QMessageBox.question(self, "Подтвердите действие",
                                             f"Начать поверку?\n"
                                             f"На калибраторе будет включен сигнал и установлены следующие параметры:\n"
                                             f"Режим измерения: Фиксированный диапазон\n"
                                             f"Тип сигнала: "
                                             f"{clb.enum_to_signal_type[self.measure_config.signal_type]}\n"
                                             f"Амплитуда: {self.highest_amplitude} {self.units_text}",
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

        self.set_amplitude(self.highest_amplitude)
        self.calibrator.mode = clb.Mode.FIXED_RANGE
        self.calibrator.signal_type = self.measure_config.signal_type
        self.calibrator.signal_enable = True

    @pyqtSlot()
    def save_point(self):
        try:
            self.measure_model.appendPoint(PointData(self.guess_point(self.calibrator.amplitude),
                                                     self.calibrator.amplitude, 0))
        except Exception as err:
            print(err)

    def guess_point(self, a_point_value):
        resolution = self.measure_config.display_resolution
        return a_point_value

    def delete_point(self):
        try:
            rows: List[QModelIndex] = self.ui.measure_table.selectionModel().selectedRows()

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

    @pyqtSlot()
    def amplitude_edit_text_changed(self):
        try:
            parsed = utils.parse_input(self.ui.amplitude_edit.text())
        except ValueError:
            parsed = ""
        qt_utils.update_edit_color(self.calibrator.amplitude, parsed, self.ui.amplitude_edit)

    @pyqtSlot()
    def apply_amplitude_button_clicked(self):
        try:
            new_amplitude = utils.parse_input(self.ui.amplitude_edit.text())
            self.set_amplitude(new_amplitude)
            self.amplitude_edit_text_changed()
        except ValueError:
            # Отлавливает некорректный ввод
            pass

    @pyqtSlot()
    def frequency_edit_text_changed(self):
        qt_utils.update_edit_color(self.calibrator.frequency, self.ui.frequency_edit.text(), self.ui.frequency_edit)

    @pyqtSlot()
    def apply_frequency_button_clicked(self):
        try:
            new_frequency = float(self.ui.frequency_edit.text())
            self.set_frequency(new_frequency)
            self.frequency_edit_text_changed()
        except ValueError:
            # Отлавливает некорректный ввод
            pass

    @pyqtSlot()
    def rough_plus_button_clicked(self):
        self.tune_amplitude(clb.AmplitudeStep.ROUGH)

    @pyqtSlot()
    def rough_minus_button_clicked(self):
        self.tune_amplitude(-clb.AmplitudeStep.ROUGH)

    @pyqtSlot()
    def common_plus_button_clicked(self):
        self.tune_amplitude(clb.AmplitudeStep.COMMON)

    @pyqtSlot()
    def common_minus_button_clicked(self):
        self.tune_amplitude(-clb.AmplitudeStep.COMMON)

    @pyqtSlot()
    def exact_plus_button_clicked(self):
        self.tune_amplitude(clb.AmplitudeStep.EXACT)

    @pyqtSlot()
    def exact_minus_button_clicked(self):
        self.tune_amplitude(-clb.AmplitudeStep.EXACT)

    @pyqtSlot()
    def fixed_plus_button_clicked(self):
        self.tune_amplitude(1)

    @pyqtSlot()
    def fixed_minus_button_clicked(self):
        self.tune_amplitude(-1)

    @pyqtSlot(QPoint)
    def show_active_table_columns(self, a_position: QPoint):
        self.header_menu.popup(self.ui.measure_table.horizontalHeader().viewport().mapToGlobal(a_position))

    @pyqtSlot(bool, int)
    def hide_selected_table_column(self, a_state, a_column):
        if a_state:
            self.ui.measure_table.showColumn(a_column)
        else:
            self.ui.measure_table.hideColumn(a_column)

    def closeEvent(self, event: QtGui.QCloseEvent):
        reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.calibrator.signal_enable = False
            # Без этого диалог не уничтожится
            for sender, connection in self.manual_connections:
                sender.triggered.disconnect(connection)
            event.accept()
        else:
            event.ignore()
