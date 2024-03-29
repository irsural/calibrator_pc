from sqlite3 import Connection

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QWheelEvent

from edit_measure_parameters_dialog import EditMeasureParamsDialog
from ui.py.measure_form import Ui_measure_dialog as MeasureForm
from measure_cases_widget import MeasureCases
from db_measures import Measure, MeasuresDB
from irspy.qt.qt_settings_ini_parser import QtSettings
from MeasureModel import PointData
import irspy.clb.calibrator_constants as clb
import constants as cfg
from irspy.qt import qt_utils
import irspy.clb.clb_dll as clb_dll
from irspy import utils


class MeasureWindow(QtWidgets.QWidget):
    remove_points = pyqtSignal(list)
    close_confirmed = pyqtSignal()

    def __init__(self, a_calibrator: clb_dll.ClbDrv, a_measure_config: Measure,
                 a_db_connection: Connection, a_settings: QtSettings,
                 a_parent: QtWidgets.QMainWindow = None):
        super().__init__(a_parent)

        self.ui = MeasureForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Калибратор N4-25. Измерение")

        self.parent = a_parent

        self.warning_animation = None
        self.pause_icon = QtGui.QIcon(QtGui.QPixmap(":/icons/icons/pause.png"))
        self.play_icon = QtGui.QIcon(QtGui.QPixmap(":/icons/icons/play.png"))
        self.ui.pause_button.setIconSize(QtCore.QSize(21, 21))

        self.set_up_icons()

        self.settings = a_settings

        self.parent.show()
        self.parent.setObjectName("measure_window")
        self.settings.restore_qwidget_state(self.parent)
        # Вызывать после self.parent.show() !!! Иначе состояние столбцов не восстановится
        self.settings.restore_qwidget_state(self.ui.measure_table)

        self.db_connection = a_db_connection

        self.calibrator = a_calibrator
        self.calibrator.signal_enable = False
        self.clb_state = clb.State.DISCONNECTED

        self.measure_config = a_measure_config
        self.measures_db = MeasuresDB(self.db_connection)
        # Нужно создать заранее, чтобы было id для сохранения меток
        self.measure_config.id = self.measures_db.new_measure(self.measure_config)

        self.measure_manager = MeasureCases(self.ui.measure_table, self.measure_config.cases,
                                            a_allow_editing=True)
        self.ui.cases_bar_layout.addWidget(self.measure_manager.cases_bar)

        # --------------------Создение переменных
        self.started = False

        self.soft_approach_points = []
        self.soft_approach_timer = QTimer(self)
        soft_approach_time_ms = 4000
        # Минимум стабильной передачи - 200 мс
        self.NEXT_SOFT_POINT_TIME_MS = 200
        self.SOFT_APPROACH_POINTS_COUNT = int(soft_approach_time_ms // self.NEXT_SOFT_POINT_TIME_MS)
        # Нужен, чтобы убедиться, что фиксированный диапазон выставлен, после чего включить сигнал
        self.start_measure_timer = QTimer(self)
        # Нужен, чтобы убедиться, что сигнал выключен, после чего менять параметры сигнала
        self.stop_measure_timer = QTimer(self)
        self.wait_dialog = None

        self.units_text = "В"
        self.value_to_user = utils.value_to_user_with_units(self.units_text)
        self.current_point = PointData()
        self.highest_amplitude = 0
        self.lowest_amplitude = 0

        self.fixed_step = 0
        self.fixed_step_list = self.settings.fixed_step_list
        # --------------------Создение переменных

        # Вызывать после создания self.measure_manager
        self.connect_signals()

        self.current_case = self.measure_manager.current_case()
        self.current_case_changed()

        self.clb_check_timer = QTimer(self)
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(100)

    def set_up_icons(self):
        self.ui.status_warning_label.hide()
        self.warning_animation = QtGui.QMovie(":/icons/gif/warning.gif")
        self.ui.status_warning_label.setMovie(self.warning_animation)
        self.warning_animation.setScaledSize(QtCore.QSize(28, 28))
        self.warning_animation.setSpeed(500)
        self.warning_animation.finished.connect(self.ui.status_warning_label.hide)

    def set_window_elements(self):
        self.ui.apply_frequency_button.setDisabled(clb.is_dc_signal[self.current_case.signal_type])
        self.ui.frequency_edit.setDisabled(clb.is_dc_signal[self.current_case.signal_type])

    def update_case_params(self):
        self.units_text = clb.signal_type_to_units[self.current_case.signal_type]
        self.value_to_user = utils.value_to_user_with_units(self.units_text)
        self.current_point = PointData()

        self.highest_amplitude = clb.bound_amplitude(utils.increase_by_percent(
            self.current_case.limit, cfg.FIRST_POINT_START_DEVIATION_PERCENT), self.current_case.signal_type)
        self.lowest_amplitude = -self.highest_amplitude if clb.is_dc_signal[self.current_case.signal_type] else 0

    def fill_fixed_step_combobox(self):
        values = self.settings.fixed_step_list

        self.ui.fixed_step_combobox.clear()
        for val in values:
            try:
                value_str = self.value_to_user(val)
                self.ui.fixed_step_combobox.addItem(value_str)
            except ValueError:
                pass
        self.ui.fixed_step_combobox.setCurrentIndex(self.settings.fixed_step_idx)

    # noinspection DuplicatedCode
    def connect_signals(self):
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)

        self.ui.start_stop_button.clicked.connect(self.start_stop_measure)
        self.ui.save_point_button.clicked.connect(self.save_point)
        self.ui.go_to_point_button.clicked.connect(self.go_to_point)
        self.ui.delete_point_button.clicked.connect(self.delete_point)
        self.remove_points.connect(self.measure_manager.view().remove_selected)

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
        self.ui.pause_button.clicked.connect(self.pause_or_resume_measure)

        self.start_measure_timer.timeout.connect(self.check_fixed_range)
        self.soft_approach_timer.timeout.connect(self.set_amplitude_soft)

        self.ui.edit_parameters_button.clicked.connect(self.update_config)

        self.measure_manager.current_case_changed.connect(self.current_case_changed)
        self.stop_measure_timer.timeout.connect(self.current_case_changed)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        self.ui.clb_list_combobox.clear()
        for clb_name in a_clb_list:
            self.ui.clb_list_combobox.addItem(clb_name)

    @pyqtSlot(clb.State)
    def update_clb_status(self, a_status: clb.State):
        self.clb_state = a_status
        self.ui.clb_state_label.setText(clb.state_to_text[a_status])

    def connect_to_clb(self, a_clb_name):
        self.calibrator.connect(a_clb_name)

    def sync_clb_parameters(self):
        if self.calibrator.amplitude_changed():
            self.show_amplitude()

        if self.calibrator.frequency_changed():
            self.show_frequency()

        self.calibrator.signal_type_changed()

        if self.calibrator.signal_type != self.current_case.signal_type:
            self.calibrator.signal_type = self.current_case.signal_type

        self.calibrator.mode_changed()

        if self.fixed_step_list != self.settings.fixed_step_list:
            self.fixed_step_list = self.settings.fixed_step_list
            self.fill_fixed_step_combobox()

    def signal_enable_changed(self, a_enable):
        if not self.started and self.calibrator.signal_enable:
            # Пока измерение не начато, запрещаем включать сигнал
            self.enable_signal(False)
            self.update_pause_button_state(False)
        else:
            if a_enable:
                self.update_pause_button_state(True)
            else:
                self.update_pause_button_state(False)

    @utils.exception_decorator_print
    def start_stop_measure(self, _):
        if not self.started:
            if self.ask_for_start_measure():
                self.started = True
                self.ui.start_stop_button.setText("Закончить\nповерку")
                self.ui.pause_button.setEnabled(True)

                self.start_measure()
        else:
            self.ask_for_close()

    def ask_for_start_measure(self):
        message = "Начать поверку?\n\n" \
                  "На калибраторе будет включен сигнал и установлены следующие параметры:\n\n" \
                  "Режим измерения: Фиксированный диапазон\n" \
                  "Тип сигнала: {0}\n" \
                  "Амплитуда: {1}".format(
            clb.signal_type_to_text[self.current_case.signal_type], self.value_to_user(self.highest_amplitude))

        if clb.is_ac_signal[self.current_case.signal_type]:
            message += "\nЧастота: {0} Гц".format(utils.float_to_string(self.calibrator.frequency))

        reply = QMessageBox.question(self, "Подтвердите действие", message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def start_measure(self):
        self.calibrator.signal_type = self.current_case.signal_type
        self.start_measure_timer.start(200)

    def update_pause_button_state(self, a_signal_enabled: bool):
        self.soft_approach_points.clear()
        if a_signal_enabled:
            self.ui.pause_button.setChecked(a_signal_enabled)
            self.ui.pause_button.setText("Пауза")
            self.ui.pause_button.setIcon(self.pause_icon)
        else:
            self.ui.pause_button.setChecked(a_signal_enabled)
            self.ui.pause_button.setText("Возобновить")
            self.ui.pause_button.setIcon(self.play_icon)

    def check_fixed_range(self):
        if self.calibrator.signal_type != self.current_case.signal_type:
            self.calibrator.signal_type = self.current_case.signal_type

        elif self.calibrator.amplitude != self.highest_amplitude:
            self.calibrator.amplitude = self.highest_amplitude

        elif self.calibrator.mode != clb.Mode.FIXED_RANGE:
            self.calibrator.mode = clb.Mode.FIXED_RANGE

        else:
            self.enable_signal(True)
            self.start_measure_timer.stop()

    @utils.exception_decorator_print
    def current_case_changed(self):
        """
        Вызывается каждый раз, когда меняются параметры сигнала
        """
        if not self.calibrator.signal_enable:
            self.current_case = self.measure_manager.current_case()
            self.set_window_elements()
            self.update_case_params()

            # Чтобы обновились единицы измерения
            self.calibrator.signal_type = self.current_case.signal_type
            self.show_amplitude()
            self.show_frequency()
            self.fill_fixed_step_combobox()

            self.stop_measure_timer.stop()
            self.close_wait_dialog()

        else:
            self.enable_signal(False)
            self.stop_measure_timer.start(1100)
            self.show_wait_dialog()

    def show_wait_dialog(self):
        if self.wait_dialog is None:
            self.wait_dialog = QtWidgets.QDialog(self)
            self.wait_dialog.setWindowTitle("Подождите")
            layout = QtWidgets.QVBoxLayout(self.wait_dialog)
            layout.addWidget(QtWidgets.QLabel("Выключается сигнал...", self.wait_dialog))
            self.wait_dialog.setFont(self.font())
            self.wait_dialog.setFixedSize(250, 50)
            self.wait_dialog.setLayout(layout)
            self.wait_dialog.adjustSize()
            self.wait_dialog.exec()

    def close_wait_dialog(self):
        if self.wait_dialog is not None:
            self.wait_dialog.close()
            self.wait_dialog = None

    def pause_or_resume_measure(self):
        if self.calibrator.signal_enable:
            self.enable_signal(False)
        else:
            # Иконка и состояние чекбокса меняется до утвердительного ответа, принудительно меняем обратно
            self.update_pause_button_state(False)
            if self.ask_for_start_measure():
                self.start_measure()

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
        self.calibrator.amplitude = utils.bound(a_amplitude, self.lowest_amplitude, self.highest_amplitude)
        self.show_amplitude()

        self.update_current_point(self.calibrator.amplitude)

    def show_amplitude(self):
        self.ui.amplitude_edit.setText(self.value_to_user(self.calibrator.amplitude))
        self.amplitude_edit_text_changed()

    def set_frequency(self, a_frequency):
        self.calibrator.frequency = a_frequency
        self.show_frequency()

        self.update_current_frequency(a_frequency)

    def show_frequency(self):
        self.ui.frequency_edit.setText(utils.float_to_string(self.calibrator.frequency))
        self.frequency_edit_text_changed()

    def tune_amplitude(self, a_step):
        self.set_amplitude(utils.relative_step_change(self.calibrator.amplitude, a_step,
                                                      clb.signal_type_to_min_step[self.current_case.signal_type],
                                                      a_normalize_value=self.current_case.limit))

    def enable_signal(self, a_signal_enable):
        self.calibrator.signal_enable = a_signal_enable
        self.update_pause_button_state(a_signal_enable)

    def update_current_point(self, a_current_value: float):
        """
        Обновляет данные, которые будут записаны в таблицу по кнопке "Сохранить точку"
        :param a_current_value: Новое значение амплитуды
        """
        self.current_point.amplitude = self.guess_point(a_current_value)

        self.current_point.approach_side = PointData.ApproachSide.UP \
            if a_current_value < self.current_point.value else PointData.ApproachSide.DOWN

        self.current_point.value = a_current_value

    def guess_point(self, a_point_value: float):
        if self.current_case.minimal_discrete == 0:
            return a_point_value
        else:
            return round(a_point_value / self.current_case.minimal_discrete) * self.current_case.minimal_discrete

    def update_current_frequency(self, a_current_frequency):
        self.current_point.frequency = a_current_frequency

    @utils.exception_decorator_print
    def save_point(self, _):
        if self.clb_state != clb.State.WAITING_SIGNAL:
            if self.measure_manager.view().is_point_measured(
                    self.current_point.amplitude, self.current_point.frequency,
                    self.current_point.approach_side):

                side_text = "СНИЗУ" if self.current_point.approach_side == PointData.ApproachSide.DOWN \
                    else "СВЕРХУ"

                point_text = "{0}".format(self.value_to_user(self.current_point.amplitude))
                if clb.is_ac_signal[self.current_case.signal_type]:
                    point_text += " : {0} Гц".format(utils.float_to_string(self.current_point.frequency))

                ask_dlg = QMessageBox(self)
                ask_dlg.setWindowTitle("Выберите действие")
                ask_dlg.setText("Значение {0} уже измерено для точки {1}.\n"
                                "Выберите действие для точки {3}({2})".format(
                    side_text, point_text, side_text, point_text))
                average_btn = ask_dlg.addButton("Усреднить", QMessageBox.YesRole)
                overwrite_btn = ask_dlg.addButton("Перезаписать", QMessageBox.YesRole)
                ask_dlg.addButton("Отменить", QMessageBox.NoRole)
                ask_dlg.exec()

                if ask_dlg.clickedButton() == overwrite_btn:
                    self.measure_manager.view().append(self.current_point)
                elif ask_dlg.clickedButton() == average_btn:
                    self.measure_manager.view().append(self.current_point, a_average=True)
            else:
                if self.clb_state == clb.State.READY:
                    self.measure_manager.view().append(self.current_point)
                else:
                    self.measure_manager.view().append(PointData(
                        a_point=self.current_point.amplitude, a_frequency=self.current_point.frequency))
        else:
            self.clb_not_ready_warning()

    def clb_not_ready_warning(self):
        QtWidgets.QApplication.beep()
        self.ui.status_warning_label.show()
        self.warning_animation.start()

    def go_to_point(self):
        rows = self.measure_manager.view().get_selected_rows()
        if rows:
            row_idx = rows[0].row()
            target_amplitude = utils.parse_input(self.measure_manager.view().get_point_by_row(row_idx))
            target_frequency = float(self.measure_manager.view().get_frequency_by_row(row_idx).replace(',', '.'))

            if target_amplitude != self.calibrator.amplitude:
                measured_up = self.measure_manager.view().is_point_measured_by_row(row_idx, PointData.ApproachSide.UP)
                measured_down = self.measure_manager.view().is_point_measured_by_row(row_idx, PointData.ApproachSide.DOWN)

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
                                                    a_normalize_value=self.current_case.limit)

                target_amplitude = utils.bound(target_amplitude, self.lowest_amplitude, self.highest_amplitude)
                target_frequency = clb.bound_frequency(target_frequency, self.current_case.signal_type)
                self.start_approach_to_point(target_amplitude, target_frequency)

    def start_approach_to_point(self, a_amplitude, a_frequency):
        if self.calibrator.signal_enable and \
                (self.calibrator.frequency == a_frequency or clb.is_dc_signal[self.current_case.signal_type]):
            self.soft_approach_points = utils.calc_smooth_approach(a_from=self.calibrator.amplitude, a_to=a_amplitude,
                                                                   a_count=self.SOFT_APPROACH_POINTS_COUNT, sigma=0.001,
                                                                   a_dt=self.NEXT_SOFT_POINT_TIME_MS)
            self.soft_approach_timer.start(self.NEXT_SOFT_POINT_TIME_MS)
        else:
            self.set_amplitude(a_amplitude)
            self.set_frequency(a_frequency)

    def set_amplitude_soft(self):
        try:
            if self.soft_approach_points:
                self.set_amplitude(self.soft_approach_points.pop(0))
            else:
                self.soft_approach_timer.stop()
        except AssertionError as err:
            print(err)

    def delete_point(self):
        rows = self.measure_manager.view().get_selected_rows()
        if rows:
            row_indexes = []
            deleted_points = ""
            for index_model in rows:
                point_str = self.measure_manager.view().get_point_by_row(index_model.row())
                deleted_points += "\n{0}".format(point_str)
                if clb.is_ac_signal[self.current_case.signal_type]:
                    freq = self.measure_manager.view().get_frequency_by_row(index_model.row())
                    deleted_points += " : {0} Гц".format(utils.float_to_string(float(freq)))

                row_indexes.append(index_model.row())

            reply = QMessageBox.question(self, "Подтвердите действие", "Удалить следующие точки?\n" +
                                         deleted_points, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.remove_points.emit(row_indexes)

    def amplitude_edit_text_changed(self):
        try:
            parsed = utils.parse_input(self.ui.amplitude_edit.text())
        except ValueError:
            parsed = ""
        qt_utils.update_edit_color(self.calibrator.amplitude, parsed, self.ui.amplitude_edit)

    def apply_amplitude_button_clicked(self):
        try:
            new_amplitude = utils.parse_input(self.ui.amplitude_edit.text())
            self.set_amplitude(new_amplitude)
        except ValueError:
            # Отлавливает некорректный ввод
            pass

    def frequency_edit_text_changed(self):
        qt_utils.update_edit_color(self.calibrator.frequency, self.ui.frequency_edit.text().replace(",", "."),
                                   self.ui.frequency_edit)

    def apply_frequency_button_clicked(self):
        try:
            new_frequency = utils.parse_input(self.ui.frequency_edit.text())
            self.set_frequency(new_frequency)
            self.frequency_edit_text_changed()
        except ValueError:
            # Отлавливает некорректный ввод
            pass

    def rough_plus_button_clicked(self):
        self.tune_amplitude(self.settings.rough_step)

    def rough_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.rough_step)

    def common_plus_button_clicked(self):
        self.tune_amplitude(self.settings.common_step)

    def common_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.common_step)

    def exact_plus_button_clicked(self):
        self.tune_amplitude(self.settings.exact_step)

    def exact_minus_button_clicked(self):
        self.tune_amplitude(-self.settings.exact_step)

    def fixed_plus_button_clicked(self):
        self.set_amplitude(self.calibrator.amplitude + self.fixed_step)

    def fixed_minus_button_clicked(self):
        self.set_amplitude(self.calibrator.amplitude - self.fixed_step)

    def set_fixed_step(self, a_new_step: str):
        try:
            self.fixed_step = utils.parse_input(a_new_step)
        except ValueError:
            self.fixed_step = 0

    @utils.exception_decorator_print
    def update_config(self, _):
        edit_template_params_dialog = EditMeasureParamsDialog(
            self.settings, self.measure_config, self.db_connection, self)
        edit_template_params_dialog.exec()

    @utils.exception_decorator_print
    def ask_for_close(self):
        reply = QMessageBox.question(self, "Подтвердите действие", "Завершить поверку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.enable_signal(False)
            # После закрытия measure_manager все кейсы синхронизированы с данными в таблицах
            self.measure_manager.close()

            if self.started:
                self.measures_db.save_measure(self.measure_config)
            else:
                self.measures_db.delete(self.measure_config.id)

            self.save_settings()

            self.close_confirmed.emit()

    def save_settings(self):
        self.settings.fixed_step_idx = self.ui.fixed_step_combobox.currentIndex()
        self.settings.save_qwidget_state(self.parent)
        self.settings.save_qwidget_state(self.ui.measure_table)

    def __del__(self):
        print(self.__class__.__name__, "deleted")
