from typing import List
import configparser

from PyQt5.QtWidgets import QMessageBox, QMenu, QAction, QTableView
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QPoint, QModelIndex, Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5 import QtCore, QtGui, QtWidgets

from QNoTemplateMeasureModel import PointData, QNoTemplateMeasureModel
from ui.py.no_template_mode_form import Ui_main_widget as NoTemplateForm
from new_no_template_measure_dialog import NoTemplateConfig
from custom_widgets.EditListDialog import EditedListWithUnits
from custom_widgets.NonOverlappingPainter import NonOverlappingPainter
import calibrator_constants as clb
import constants as cfg
import clb_dll
import utils
import qt_utils


class NoTemplateWindow(QtWidgets.QWidget):
    remove_points = pyqtSignal(list)
    close_confirmed = pyqtSignal()

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: NoTemplateConfig,
                 a_settings: configparser.ConfigParser, a_parent=None):
        super().__init__(a_parent)

        self.ui = NoTemplateForm()

        self.ui.setupUi(self)

        pause_icon = QtGui.QIcon()
        pause_icon.addPixmap(QtGui.QPixmap(cfg.PAUSE_ICON_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
        pause_icon.addPixmap(QtGui.QPixmap(cfg.PLAY_ICON_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pause_button.setIcon(pause_icon)
        self.ui.pause_button.setIconSize(QtCore.QSize(21, 21))

        self.ui.status_warning_label.hide()
        self.warning_animation = QtGui.QMovie(cfg.WARNING_GIF_PATH)
        self.ui.status_warning_label.setMovie(self.warning_animation)
        self.warning_animation.setScaledSize(QtCore.QSize(28, 28))
        self.warning_animation.setSpeed(500)
        self.warning_animation.finished.connect(self.ui.status_warning_label.hide)

        self.show()

        self.measure_config: NoTemplateConfig = a_measure_config
        self.settings = a_settings

        self.units_text = clb.signal_type_to_units[self.measure_config.signal_type]
        self.value_to_user = utils.value_to_user_with_units(self.units_text)
        self.current_point = PointData(a_normalize_value=self.measure_config.upper_bound)
        self.start_button_active = True
        self.soft_approach_points = []
        self.soft_approach_timer = QTimer()
        # Минимум стабильной передачи - 200 мс
        self.next_soft_point_time_ms = 200
        self.soft_approach_time_s = 4
        # Нужен, чтобы убедиться, что фиксированный диапазон выставлен, после чего включить сигнал
        self.start_measure_timer = QTimer(self)

        self.calibrator = a_calibrator
        self.clb_state = clb.State.DISCONNECTED
        self.calibrator.signal_type = self.measure_config.signal_type

        self.highest_amplitude = utils.increase_by_percent(self.measure_config.upper_bound,
                                                           self.measure_config.start_deviation)
        self.lowest_amplitude = -self.highest_amplitude if clb.is_dc_signal[self.measure_config.signal_type] else 0

        self.highest_amplitude = self.calibrator.limit_amplitude(self.highest_amplitude, self.lowest_amplitude,
                                                                 self.highest_amplitude)

        self.measure_model = QNoTemplateMeasureModel(self.current_point.normalize_value,
                                                     a_error_limit=self.measure_config.accuracy_class,
                                                     a_value_units=self.units_text,
                                                     a_parent=self)
        self.ui.measure_table.setModel(self.measure_model)
        self.ui.measure_table.setItemDelegate(NonOverlappingPainter(self))

        self.set_window_elements()
        # Обязательно вызывать после set_window_elements иначе будет рассинхрон галочек хэдера и отображаемых колонок
        self.header_menu, self.manual_connections = self.create_table_header_context_menu(self.ui.measure_table)

        self.fixed_step = 0
        self.fixed_range_amplitudes_list = self.settings[cfg.NO_TEMPLATE_SECTION][cfg.FIXED_RANGES_KEY].split(',')
        self.fill_fixed_step_combobox(self.fixed_range_amplitudes_list, a_save=False)

        # Вызывать после создания self.measure_model и после self.fill_fixed_step_combobox
        self.connect_signals()

        self.clb_check_timer = QTimer(self)
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)

        self.window_existing_timer = QtCore.QTimer(self)
        self.window_existing_timer.timeout.connect(self.window_existing_check)
        self.window_existing_timer.start(3000)

    def window_existing_check(self):
        print("No template window")

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
        if clb.is_dc_signal[self.measure_config.signal_type]:
            self.ui.apply_frequency_button.setDisabled(True)
            self.ui.frequency_edit.setDisabled(True)
            self.ui.measure_table.hideColumn(QNoTemplateMeasureModel.Column.FREQUENCY)

        self.setWindowTitle(f"{self.measure_config.clb_name}. "
                            f"{clb.enum_to_signal_type[self.measure_config.signal_type]}. "
                            f"{self.measure_config.upper_bound} {self.units_text}.")

        if self.measure_config.auto_calc_points:
            if self.measure_config.start_point_side == NoTemplateConfig.StartPoint.LOWER:
                calculated_points = utils.auto_calc_points(self.measure_config.lower_bound,
                                                           self.measure_config.upper_bound,
                                                           self.measure_config.points_step)
            else:
                calculated_points = utils.auto_calc_points(self.measure_config.upper_bound,
                                                           self.measure_config.lower_bound,
                                                           self.measure_config.points_step)

            for point in calculated_points:
                self.measure_model.appendPoint(PointData(a_point=point))

    @pyqtSlot(list)
    def fill_fixed_step_combobox(self, a_values: List[float], a_save=True):
        save_string = ""
        self.ui.fixed_step_combobox.clear()
        a_values.sort()

        for val in a_values:
            try:
                value_str = self.value_to_user(float(val))
            except ValueError:
                value_str = self.value_to_user(0)

            if self.ui.fixed_step_combobox.findText(value_str) == -1:
                self.ui.fixed_step_combobox.addItem(value_str)
                save_string += f"{val},"

        if a_save:
            save_string = save_string.strip(',')
            self.settings[cfg.NO_TEMPLATE_SECTION][cfg.FIXED_RANGES_KEY] = save_string
            utils.save_settings(cfg.CONFIG_PATH, self.settings)

    @pyqtSlot()
    def edit_fixed_step(self):
        current_ranges = \
            tuple(self.ui.fixed_step_combobox.itemText(ind) for ind in range(self.ui.fixed_step_combobox.count()))
        edit_ranges_dialog = EditedListWithUnits(self.units_text, self, current_ranges,
                                                 "Редактирование фиксированного шага", "Шаг")
        edit_ranges_dialog.list_ready.connect(self.fill_fixed_step_combobox)

    def connect_signals(self):
        self.ui.start_stop_button.clicked.connect(self.start_stop_measure)
        self.ui.save_point_button.clicked.connect(self.save_point)
        self.ui.go_to_point_button.clicked.connect(self.go_to_point)
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

        self.ui.fixed_step_combobox.currentTextChanged.connect(self.set_fixed_step)
        self.ui.pause_button.toggled.connect(self.pause_start_signal)

        self.ui.zero_deviation_edit.editingFinished.connect(self.ui.zero_deviation_edit.clearFocus)
        self.start_measure_timer.timeout.connect(self.check_fixed_range)

        self.soft_approach_timer.timeout.connect(self.set_amplitude_soft)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        pass

    @pyqtSlot(clb.State)
    def update_clb_status(self, a_status: clb.State):
        self.clb_state = a_status
        self.ui.clb_state_label.setText(clb.enum_to_state[a_status])

    def sync_clb_parameters(self):
        if self.calibrator.amplitude_changed():
            self.set_amplitude(self.calibrator.amplitude)

        if self.calibrator.frequency_changed():
            self.set_frequency(self.calibrator.frequency)

        if self.start_button_active and self.calibrator.signal_enable:
            # Пока измерение не начато, запрещаем включать сигнал
            self.calibrator.signal_enable = False

        # Эта переменная синхронизируется в startwindow.py
        if self.calibrator.signal_enable:
            self.ui.pause_button.setChecked(True)
        else:
            self.ui.pause_button.setChecked(False)

        if self.calibrator.signal_type_changed():
            if self.calibrator.signal_type != self.measure_config.signal_type:
                self.calibrator.signal_type = self.measure_config.signal_type

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if self.ui.measure_table.hasFocus():
            key = event.key()
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                rows: List[QModelIndex] = self.get_selected_rows()
                if rows:
                    self.ui.measure_table.edit(rows[0])
        else:
            event.accept()

    def wheelEvent(self, event: QWheelEvent):
        steps = qt_utils.get_wheel_steps(event)
        keys = event.modifiers()
        if (keys & Qt.ControlModifier) and (keys & Qt.ShiftModifier):
            self.set_amplitude(self.calibrator.amplitude + (self.fixed_step * steps))
        elif keys & Qt.ShiftModifier:
            self.tune_amplitude(clb.AmplitudeStep.EXACT * steps)
        elif keys & Qt.ControlModifier:
            self.tune_amplitude(clb.AmplitudeStep.ROUGH * steps)
        else:
            self.tune_amplitude(clb.AmplitudeStep.COMMON * steps)

        event.accept()

    def set_amplitude(self, a_amplitude: float):
        self.calibrator.amplitude = self.calibrator.limit_amplitude(a_amplitude, self.lowest_amplitude,
                                                                    self.highest_amplitude)
        self.ui.amplitude_edit.setText(self.value_to_user(self.calibrator.amplitude))

        self.amplitude_edit_text_changed()
        self.update_current_point(self.calibrator.amplitude)

    def set_amplitude_soft(self):
        try:
            if self.soft_approach_points:
                self.set_amplitude(self.soft_approach_points.pop(0))
            else:
                self.soft_approach_timer.stop()
        except AssertionError as err:
            print(err)

    def set_frequency(self, a_frequency):
        self.calibrator.frequency = a_frequency
        current_frequency = 0 if clb.is_dc_signal[self.measure_config.signal_type] else self.calibrator.frequency
        self.ui.frequency_edit.setText(utils.float_to_string(current_frequency))

        self.update_current_frequency(current_frequency)

    def tune_amplitude(self, a_step):
        self.set_amplitude(utils.relative_step_change(self.calibrator.amplitude, a_step,
                                                      clb.signal_type_to_min_step[self.measure_config.signal_type],
                                                      a_normalize_value=self.measure_config.upper_bound))

    def update_current_point(self, a_current_value: float):
        """
        Обновляет данные, которые будут записаны в таблицу по кнопке "Сохранить точку"
        :param a_current_value: Новое значение амплитуды
        """
        self.current_point.point = self.guess_point(a_current_value)
        self.current_point.prev_value = self.current_point.value

        self.current_point.approach_side = PointData.ApproachSide.UP \
            if a_current_value < self.current_point.value else PointData.ApproachSide.DOWN

        self.current_point.value = a_current_value

    def update_current_frequency(self, a_current_frequency):
        self.current_point.frequency = a_current_frequency

    @pyqtSlot()
    def start_stop_measure(self):
        if self.start_button_active:
            reply = QMessageBox.question(self, "Подтвердите действие",
                                         f"Начать поверку?\n\n"
                                         f"На калибраторе будет включен сигнал и установлены следующие параметры:\n\n"
                                         f"Режим измерения: Фиксированный диапазон\n"
                                         f"Тип сигнала: "
                                         f"{clb.enum_to_signal_type[self.measure_config.signal_type]}\n"
                                         f"Амплитуда: {self.value_to_user(self.highest_amplitude)}",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.start_button_active = False
                self.start_measure()
        else:
            self.ask_for_close()

    def start_measure(self):
        self.ui.start_stop_button.setText("Закончить\nповерку")
        self.ui.pause_button.setEnabled(True)

        self.set_amplitude(self.highest_amplitude)
        self.calibrator.mode = clb.Mode.FIXED_RANGE
        self.calibrator.signal_type = self.measure_config.signal_type
        # self.calibrator.signal_enable = True

        self.start_measure_timer.start(1100)

    @pyqtSlot()
    def save_point(self):
        if self.clb_state == clb.State.READY:
            try:
                if self.measure_model.isPointGood(self.current_point.point, self.current_point.approach_side):
                    side_text = "СНИЗУ" if self.current_point.approach_side == PointData.ApproachSide.DOWN \
                        else "СВЕРХУ"
                    reply = QMessageBox.question(self, "Подтвердите действие", f"Значение {side_text} уже измерено "
                                                 f"для точки {self.value_to_user(self.current_point.point)} и не превышает "
                                                 f"допустимую погрешность. Перезаписать значение {side_text} для точки "
                                                 f"{self.value_to_user(self.current_point.point)} ?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.update_table(self.current_point)
                else:
                    self.update_table(self.current_point)
            except AssertionError as err:
                print(err)
        else:
            self.clb_not_ready_warning()

    def update_table(self, a_point: PointData):
        point_row = self.measure_model.appendPoint(a_point)
        self.ui.measure_table.selectRow(point_row)

    def clb_not_ready_warning(self):
        QtWidgets.QApplication.beep()
        self.ui.status_warning_label.show()
        self.warning_animation.start()

    def go_to_point(self):
        rows = self.get_selected_rows()
        if rows:
            row_idx = rows[0].row()
            measured_up = self.measure_model.isPointMeasured(row_idx, PointData.ApproachSide.UP)
            measured_down = self.measure_model.isPointMeasured(row_idx, PointData.ApproachSide.DOWN)

            target_amplitude = self.measure_model.getPointByRow(row_idx)

            if measured_down == measured_up:
                # Точка измерена полностью либо совсем не измерена, подходим с ближайшей стороны
                if self.calibrator.amplitude > target_amplitude:
                    target_amplitude = utils.increase_by_percent(target_amplitude, self.measure_config.start_deviation,
                                                                 a_normalize_value=self.measure_config.upper_bound)
                else:
                    target_amplitude = utils.decrease_by_percent(target_amplitude, self.measure_config.start_deviation,
                                                                 a_normalize_value=self.measure_config.upper_bound)
            else:
                if measured_up:
                    target_amplitude = utils.decrease_by_percent(target_amplitude, self.measure_config.start_deviation,
                                                                 a_normalize_value=self.measure_config.upper_bound)
                else:
                    target_amplitude = utils.increase_by_percent(target_amplitude, self.measure_config.start_deviation,
                                                                 a_normalize_value=self.measure_config.upper_bound)

            target_amplitude = self.calibrator.limit_amplitude(target_amplitude, self.lowest_amplitude,
                                                               self.highest_amplitude)

            if self.calibrator.signal_enable:
                points_count = int((self.soft_approach_time_s * 1000) // self.next_soft_point_time_ms)
                self.soft_approach_points = utils.calc_smooth_approach(a_from=self.calibrator.amplitude,
                                                                       a_to=target_amplitude,
                                                                       a_count=points_count,
                                                                       a_dt=self.next_soft_point_time_ms,
                                                                       sigma=0.001)
                print(self.soft_approach_points)
                self.soft_approach_timer.start(self.next_soft_point_time_ms)
            else:
                self.set_amplitude(target_amplitude)

    def guess_point(self, a_point_value: float):
        return round(a_point_value / self.measure_config.minimal_discrete) * self.measure_config.minimal_discrete

    def delete_point(self):
        rows = self.get_selected_rows()
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

    def get_selected_rows(self) -> List[QModelIndex]:
        return self.ui.measure_table.selectionModel().selectedRows()

    def get_table_item_by_index(self, a_row: int, a_column: int):
        index = self.measure_model.index(a_row, a_column)
        data = self.measure_model.data(index)
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
        except ValueError:
            # Отлавливает некорректный ввод
            pass

    @pyqtSlot()
    def frequency_edit_text_changed(self):
        qt_utils.update_edit_color(self.calibrator.frequency, self.ui.frequency_edit.text().replace(",", "."),
                                   self.ui.frequency_edit)

    @pyqtSlot()
    def apply_frequency_button_clicked(self):
        try:
            new_frequency = utils.parse_input(self.ui.frequency_edit.text())
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
        self.set_amplitude(self.calibrator.amplitude + self.fixed_step)

    @pyqtSlot()
    def fixed_minus_button_clicked(self):
        self.set_amplitude(self.calibrator.amplitude - self.fixed_step)

    @pyqtSlot(bool)
    def pause_start_signal(self, a_enabled: bool):
        self.soft_approach_points.clear()

        if a_enabled:
            self.ui.pause_button.setText("Пауза")
            self.calibrator.signal_enable = True

        else:
            self.calibrator.signal_enable = False
            self.ui.pause_button.setText("Возобновить")

    @pyqtSlot(QPoint)
    def show_active_table_columns(self, a_position: QPoint):
        self.header_menu.popup(self.ui.measure_table.horizontalHeader().viewport().mapToGlobal(a_position))

    @pyqtSlot(str)
    def set_fixed_step(self, a_new_step: str):
        try:
            self.fixed_step = utils.parse_input(a_new_step)
        except ValueError:
            self.fixed_step = 0

    @pyqtSlot(bool, int)
    def hide_selected_table_column(self, a_state, a_column):
        if a_state:
            self.ui.measure_table.showColumn(a_column)
        else:
            self.ui.measure_table.hideColumn(a_column)

    @pyqtSlot()
    def check_fixed_range(self):
        if self.calibrator.mode == clb.Mode.FIXED_RANGE and self.calibrator.amplitude == self.highest_amplitude:
            self.calibrator.signal_enable = True
            self.start_measure_timer.stop()

    def ask_for_close(self):
        reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.calibrator.signal_enable = False

            # Без этого диалог не уничтожится
            for sender, connection in self.manual_connections:
                sender.triggered.disconnect(connection)

            self.close_confirmed.emit()
