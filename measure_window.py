from sqlite3 import Connection
from typing import List

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QWheelEvent

from edit_measure_parameters_dialog import EditMeasureParamsDialog
from db_measures import MeasureParams, MeasureTables, MeasuresDB
from ui.py.measure_form import Ui_main_widget as MeasureForm
from MeasureModel import PointData
from MeasureView import MeasureView
from settings_ini_parser import Settings
import calibrator_constants as clb
import constants as cfg
import clb_dll
import utils
import qt_utils


class MeasureWindow(QtWidgets.QWidget):
    remove_points = pyqtSignal(list)
    close_confirmed = pyqtSignal()

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: MeasureParams, a_db_connection: Connection,
                 a_db_tables: MeasureTables, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = MeasureForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.warning_animation = None
        self.set_up_icons()

        self.settings = a_settings

        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.parent.show()
        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        # Вызывать после self.parent.show() !!! Иначе состояние столбцов не восстановится
        self.ui.measure_table.horizontalHeader().restoreState(self.settings.get_last_header_state(
            self.__class__.__name__))

        self.db_connection = a_db_connection
        self.db_tables = a_db_tables

        self.measures_db = MeasuresDB(self.db_connection, self.db_tables)
        self.measure_config: MeasureParams = a_measure_config
        self.measure_config.id = self.measures_db.create()
        self.measure_config.time = QtCore.QTime.currentTime().toString("H:mm:ss")

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
        self.started = False

        self.calibrator = a_calibrator
        self.clb_state = clb.State.DISCONNECTED
        self.calibrator.signal_type = self.measure_config.signal_type

        self.highest_amplitude = utils.increase_by_percent(self.measure_config.upper_bound,
                                                           self.settings.start_deviation)
        self.lowest_amplitude = -self.highest_amplitude if clb.is_dc_signal[self.measure_config.signal_type] else 0
        self.highest_amplitude = self.calibrator.limit_amplitude(self.highest_amplitude, self.lowest_amplitude,
                                                                 self.highest_amplitude)

        self.measure_view = MeasureView(self.ui.measure_table, self.measure_config, self.current_point.normalize_value)

        self.set_window_elements()

        self.fixed_step = 0
        self.fixed_step_list = self.settings.fixed_step_list
        self.fill_fixed_step_combobox()
        self.settings.fixed_step_changed.connect(self.fill_fixed_step_combobox)

        # Вызывать после создания self.measure_view и после self.fill_fixed_step_combobox
        self.connect_signals()

        self.clb_check_timer = QTimer(self)
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)

    def set_up_icons(self):
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

    def set_window_elements(self):
        self.ui.apply_frequency_button.setDisabled(clb.is_dc_signal[self.measure_config.signal_type])
        self.ui.frequency_edit.setDisabled(clb.is_dc_signal[self.measure_config.signal_type])

        self.setWindowTitle(f"{clb.enum_to_signal_type[self.measure_config.signal_type]}. "
                            f"{self.measure_config.upper_bound} {self.units_text}.")

    def fill_fixed_step_combobox(self):
        values: List[float] = self.settings.fixed_step_list

        self.ui.fixed_step_combobox.clear()
        for val in values:
            try:
                value_str = self.value_to_user(val)
                self.ui.fixed_step_combobox.addItem(value_str)
            except ValueError:
                pass

    # noinspection DuplicatedCode
    def connect_signals(self):
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)

        self.ui.start_stop_button.clicked.connect(self.start_stop_measure)
        self.ui.save_point_button.clicked.connect(self.save_point)
        self.ui.go_to_point_button.clicked.connect(self.go_to_point)
        self.ui.delete_point_button.clicked.connect(self.delete_point)
        self.remove_points.connect(self.measure_view.remove_selected)

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

        self.start_measure_timer.timeout.connect(self.check_fixed_range)
        self.soft_approach_timer.timeout.connect(self.set_amplitude_soft)

        self.ui.edit_parameters_button.clicked.connect(self.update_config)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        self.ui.clb_list_combobox.clear()
        for clb_name in a_clb_list:
            self.ui.clb_list_combobox.addItem(clb_name)

    @pyqtSlot(clb.State)
    def update_clb_status(self, a_status: clb.State):
        self.clb_state = a_status
        self.ui.clb_state_label.setText(clb.enum_to_state[a_status])

    def connect_to_clb(self, a_clb_name):
        self.calibrator.connect(a_clb_name)

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

    # def keyPressEvent(self, event: QtGui.QKeyEvent):
    #     if self.ui.measure_table.hasFocus():
    #         key = event.key()
    #         if key == Qt.Key_Return or key == Qt.Key_Enter:
    #             rows: List[QModelIndex] = self.get_selected_rows()
    #             if rows:
    #                 self.ui.measure_table.edit(rows[0])
    #     else:
    #         event.accept()

    def wheelEvent(self, event: QWheelEvent):
        if not (self.ui.measure_table.underMouse() and self.settings.disable_scroll_on_table):
            steps = qt_utils.get_wheel_steps(event)
            steps = -steps if self.settings.mouse_inversion else steps

            keys = event.modifiers()
            if (keys & Qt.ControlModifier) and (keys & Qt.ShiftModifier):
                self.set_amplitude(self.calibrator.amplitude + (self.fixed_step * steps))
            elif keys & Qt.ShiftModifier:
                self.tune_amplitude(self.settings.exact_step * steps)
            elif keys & Qt.ControlModifier:
                self.tune_amplitude(self.settings.rough_step * steps)
            else:
                self.tune_amplitude(self.settings.common_step * steps)

        event.accept()

    def set_amplitude(self, a_amplitude: float):
        self.calibrator.amplitude = self.calibrator.limit_amplitude(a_amplitude, self.lowest_amplitude,
                                                                    self.highest_amplitude)
        self.ui.amplitude_edit.setText(self.value_to_user(self.calibrator.amplitude))

        self.amplitude_edit_text_changed()
        self.update_current_point(self.calibrator.amplitude)

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

        self.current_point.approach_side = PointData.ApproachSide.UP \
            if a_current_value < self.current_point.value else PointData.ApproachSide.DOWN

        self.current_point.value = a_current_value

    def update_current_frequency(self, a_current_frequency):
        self.current_point.frequency = a_current_frequency

    @pyqtSlot()
    def start_stop_measure(self):
        if self.start_button_active:
            message = f"Начать поверку?\n\n" \
                      f"На калибраторе будет включен сигнал и установлены следующие параметры:\n\n"\
                      f"Режим измерения: Фиксированный диапазон\n"\
                      f"Тип сигнала: {clb.enum_to_signal_type[self.measure_config.signal_type]}\n"\
                      f"Амплитуда: {self.value_to_user(self.highest_amplitude)}"

            if clb.is_ac_signal[self.measure_config.signal_type]:
                message += f"\nЧастота: {utils.float_to_string(self.calibrator.frequency)} Гц"

            reply = QMessageBox.question(self, "Подтвердите действие", message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

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
        self.started = True

        self.start_measure_timer.start(1100)

    @pyqtSlot()
    def save_point(self):
        if self.clb_state != clb.State.WAITING_SIGNAL:
            try:
                if self.measure_view.is_point_good(self.current_point.point, self.current_point.frequency,
                                                   self.current_point.approach_side):

                    side_text = "СНИЗУ" if self.current_point.approach_side == PointData.ApproachSide.DOWN \
                        else "СВЕРХУ"

                    point_text = f"{self.value_to_user(self.current_point.point)}"
                    if clb.is_ac_signal[self.measure_config.signal_type]:
                        point_text += f" : {utils.float_to_string(self.current_point.frequency)} Гц"

                    reply = QMessageBox.question(self, "Подтвердите действие", f"Значение {side_text} уже измерено "
                                                 f"для точки {point_text} и не превышает допустимую погрешность. "
                                                 f"Перезаписать значение {side_text} для точки {point_text}?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.measure_view.append(self.current_point)
                else:
                    if self.clb_state == clb.State.READY:
                        self.measure_view.append(self.current_point)
                    else:
                        self.measure_view.append(PointData(a_point=self.current_point.point,
                                                           a_frequency=self.current_point.frequency))
            except AssertionError as err:
                print(err)
        else:
            self.clb_not_ready_warning()

    def clb_not_ready_warning(self):
        QtWidgets.QApplication.beep()
        self.ui.status_warning_label.show()
        self.warning_animation.start()

    def go_to_point(self):
        rows = self.measure_view.get_selected_rows()
        if rows:
            row_idx = rows[0].row()
            target_amplitude = utils.parse_input(self.measure_view.get_point_by_row(row_idx))

            if target_amplitude != self.calibrator.amplitude:
                measured_up = self.measure_view.is_point_measured(row_idx, PointData.ApproachSide.UP)
                measured_down = self.measure_view.is_point_measured(row_idx, PointData.ApproachSide.DOWN)

                if measured_down == measured_up:
                    # Точка измерена полностью либо совсем не измерена, подходим с ближайшей стороны
                    if self.calibrator.amplitude > target_amplitude:
                        change_value_foo = utils.increase_by_percent
                    else:
                        change_value_foo = utils.decrease_by_percent
                else:
                    if measured_up:
                        change_value_foo = utils.decrease_by_percent
                    else:
                        change_value_foo = utils.increase_by_percent

                target_amplitude = change_value_foo(target_amplitude, self.settings.start_deviation,
                                                    a_normalize_value=self.measure_config.upper_bound)

                target_amplitude = self.calibrator.limit_amplitude(target_amplitude, self.lowest_amplitude,
                                                                   self.highest_amplitude)
                self.start_approach_to_point(target_amplitude)

    def start_approach_to_point(self, a_point):
        if self.calibrator.signal_enable:
            points_count = int((self.soft_approach_time_s * 1000) // self.next_soft_point_time_ms)
            self.soft_approach_points = utils.calc_smooth_approach(a_from=self.calibrator.amplitude, a_to=a_point,
                                                                   a_count=points_count, sigma=0.001,
                                                                   a_dt=self.next_soft_point_time_ms)
            self.soft_approach_timer.start(self.next_soft_point_time_ms)
        else:
            self.set_amplitude(a_point)

    def set_amplitude_soft(self):
        try:
            if self.soft_approach_points:
                self.set_amplitude(self.soft_approach_points.pop(0))
            else:
                self.soft_approach_timer.stop()
        except AssertionError as err:
            print(err)

    def guess_point(self, a_point_value: float):
        if self.measure_config.minimal_discrete == 0:
            return a_point_value
        else:
            return round(a_point_value / self.measure_config.minimal_discrete) * self.measure_config.minimal_discrete

    def delete_point(self):
        rows = self.measure_view.get_selected_rows()
        if rows:
            row_indexes = []
            deleted_points = ""
            for index_model in rows:
                point_str = self.measure_view.get_point_by_row(index_model.row())
                deleted_points += f"\n{point_str}"
                if clb.is_ac_signal[self.measure_config.signal_type]:
                    freq = self.measure_view.get_frequency_by_row(index_model.row())
                    deleted_points += f" : {utils.float_to_string(float(freq))} Гц"

                row_indexes.append(index_model.row())

            reply = QMessageBox.question(self, "Подтвердите действие", "Удалить следующие точки?\n" +
                                         deleted_points, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.remove_points.emit(row_indexes)

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
        self.tune_amplitude(self.settings.rough_step)

    @pyqtSlot()
    def rough_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.rough_step)

    @pyqtSlot()
    def common_plus_button_clicked(self):
        self.tune_amplitude(self.settings.common_step)

    @pyqtSlot()
    def common_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.common_step)

    @pyqtSlot()
    def exact_plus_button_clicked(self):
        self.tune_amplitude(self.settings.exact_step)

    @pyqtSlot()
    def exact_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.exact_step)

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

    @pyqtSlot(str)
    def set_fixed_step(self, a_new_step: str):
        try:
            self.fixed_step = utils.parse_input(a_new_step)
        except ValueError:
            self.fixed_step = 0

    @pyqtSlot()
    def check_fixed_range(self):
        if self.calibrator.mode == clb.Mode.FIXED_RANGE and self.calibrator.amplitude == self.highest_amplitude:
            self.calibrator.signal_enable = True
            self.start_measure_timer.stop()

    def update_config(self):
        try:
            edit_template_params_dialog = EditMeasureParamsDialog(self.settings, self.measure_config,
                                                                  self.db_connection, self.db_tables, self)
            edit_template_params_dialog.exec()

            self.measure_view.set_device_class(self.measure_config.device_class)
        except AssertionError as err:
            utils.exception_handler(err)

    def ask_for_close(self):
        try:
            reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.calibrator.signal_enable = False
                if self.started:
                    self.measure_config.points = self.measure_view.export_points()
                    self.measures_db.save(self.measure_config, True)
                else:
                    self.measures_db.delete(self.measure_config.id)

                self.save_settings()
                self.measure_view.close()

                self.close_confirmed.emit()
        except AssertionError as err:
            utils.exception_handler(err)

    def save_settings(self):
        self.settings.fixed_step_idx = self.ui.fixed_step_combobox.currentIndex()

        self.settings.save_geometry(self.__class__.__name__, self.parent.saveGeometry())
        self.settings.save_header_state(self.__class__.__name__, self.ui.measure_table.horizontalHeader().saveState())

    def __del__(self):
        print(self.__class__.__name__, "deleted")
