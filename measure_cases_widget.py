from typing import List, Tuple, Iterable

from PyQt5 import QtCore, QtWidgets, QtGui

from MeasureView import MeasureView
from MeasureModel import MeasureModel
from db_measures import Measure
from edit_case_params_dialog import EditCaseParamsDialog
import irspy.clb.calibrator_constants as clb
from irspy import utils


class MeasureCases(QtWidgets.QWidget):
    case_added = QtCore.pyqtSignal()
    case_removed = QtCore.pyqtSignal(int)
    current_case_changed = QtCore.pyqtSignal()

    def __init__(self, a_case_table: QtWidgets.QTableView, a_cases: List[Measure.Case], a_allow_editing, a_parent=None):
        super().__init__(a_parent)

        self.allow_editing = a_allow_editing
        self.parent = a_parent

        self.cases_bar = QtWidgets.QTabBar(self)
        self.set_up_tab_widget()

        assert a_cases, "Every measure must have at least 1 case!!!"
        self.measure_view = MeasureView(a_case_table, a_cases[0])

        self.cases = a_cases
        for case in self.cases:
            self.add_new_tab(case)

        self.select_case(0)
        # noinspection PyUnresolvedReferences
        self.cases_bar.currentChanged.connect(self.select_case)

    def __del__(self):
        print("measure cases deleted")

    def view(self):
        return self.measure_view

    def set_up_tab_widget(self):
        self.cases_bar.setStyleSheet(
            "QTabBar::tab:last { margin-right: 2px; margin-left:0px; padding-left: 0; }\n"
            "QTabBar::tab:selected { background: white; border: 1px solid #000000; border-bottom: 0; }\n"
            "QTabBar::tab { padding-left: 6px; height: 30px }")

        self.cases_bar.setExpanding(False)

        plus_button = QtWidgets.QPushButton()
        plus_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/icons/plus.png")))
        plus_button.setFlat(True)
        plus_button.setFixedSize(30, 30)
        self.cases_bar.addTab("")
        self.cases_bar.setTabEnabled(self.cases_bar.count() - 1, False)
        self.cases_bar.setTabButton(self.cases_bar.count() - 1, QtWidgets.QTabBar.RightSide, plus_button)
        plus_button.clicked.connect(self.plus_button_clicked)
        plus_button.setEnabled(self.allow_editing)

    def plus_button_clicked(self):
        self.add_new_tab()

    @utils.exception_decorator_print
    def select_case(self, a_idx):
        self.cases_bar.setCurrentIndex(a_idx)
        self.measure_view.reset(self.cases[a_idx])
        self.current_case_changed.emit()

    @utils.exception_decorator_print
    def add_new_tab(self, a_case: Measure.Case = None):
        if a_case is None:
            a_case = Measure.Case()
            self.cases.append(a_case)

        settings_close_widget = SettingsCloseWidget(self.cases_bar)
        settings_close_widget.settings_clicked.connect(self.open_case_settings)
        settings_close_widget.close_clicked.connect(self.delete_case)
        settings_close_widget.setEnabled(self.allow_editing)

        new_tab_index = self.cases_bar.count() - 1
        self.cases_bar.insertTab(new_tab_index, self.create_tab_name(a_case))
        self.cases_bar.setTabButton(new_tab_index, QtWidgets.QTabBar.RightSide, settings_close_widget)

        self.cases_bar.setCurrentIndex(new_tab_index)

    def open_case_settings(self):
        sender = self.sender()
        tab_idx = self.get_tab_idx(sender)
        self.edit_case_parameters(tab_idx)

    @utils.exception_decorator_print
    def delete_case(self, _):
        sender = self.sender()
        tab_idx = self.get_tab_idx(sender)
        self.remove_tab(tab_idx)

        if self.cases_bar.currentIndex() == tab_idx:
            # В этих случаях cases_bar.currentChanged не эмитится
            self.select_case(tab_idx)

    def get_tab_idx(self, a_widget):
        for tab_idx in range(self.cases_bar.count() - 1):
            if a_widget is self.cases_bar.tabButton(tab_idx, QtWidgets.QTabBar.RightSide):
                return tab_idx
        assert True, "Cant find tab idx by widget!!!"

    @staticmethod
    def create_tab_name(a_case: Measure.Case):
        return " " + clb.signal_type_to_text_short[a_case.signal_type] + "; " + \
               utils.value_to_user_with_units(clb.signal_type_to_units[a_case.signal_type])(a_case.limit)

    @utils.exception_decorator_print
    def remove_tab(self, a_idx: int):
        if self.cases_bar.count() > 2:
            tab_name = self.cases_bar.tabText(self.cases_bar.currentIndex())
            res = QtWidgets.QMessageBox.question(
                self, "Подтвердите действие",
                "Вы действительно хотите удалить измерение {0}?".format(tab_name),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.Yes:
                if a_idx == self.cases_bar.count() - 2 and a_idx == self.cases_bar.currentIndex():
                    # Если удаляемая вкладка активна, меняем активную на предыдущую
                    self.cases_bar.setCurrentIndex(self.cases_bar.count() - 3)

                self.cases_bar.removeTab(a_idx)
                self.cases.pop(a_idx)

    @utils.exception_decorator_print
    def edit_case_parameters(self, a_case_number):
        case = self.cases[a_case_number]
        case_params_dialog = EditCaseParamsDialog(case, self)

        if case_params_dialog.exec() == QtWidgets.QDialog.Accepted:
            self.cases_bar.setTabText(a_case_number, self.create_tab_name(case))

            if self.cases_bar.currentIndex() == a_case_number:
                # Обновляем параметры измерения
                self.select_case(a_case_number)

    def current_case(self):
        return self.cases[self.cases_bar.currentIndex()]

    def export_tables(self) -> List[Tuple[Measure.Case, Iterable]]:
        """
        Возвращает пару Measure.Case и данных таблиц в их текущем визуальном состоянии (Учитывая скрытые колонки и
        положение колонок)
        Не учитывается только колонка частоты (Она всегда добавляется в качестве последней колонки)
        """
        table = self.measure_view.view()
        chosen_column = []
        for column in range(table.horizontalHeader().count()):
            logic_column = table.horizontalHeader().logicalIndex(column)
            if not table.isColumnHidden(logic_column):
                # Частота всегда добавляется в конец
                if logic_column != MeasureModel.Column.FREQUENCY:
                    chosen_column.append(logic_column)
        chosen_column.append(MeasureModel.Column.FREQUENCY)

        case_data = []
        for case in self.cases:
            model = MeasureModel(a_normalize_value=case.limit, a_error_limit=case.device_class,
                                 a_signal_type=case.signal_type, a_init_points=case.points, a_parent=table)
            case_data.append((case, model.exportByColumns(chosen_column)))

        return case_data

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.measure_view.close()
        a_event.accept()


class SettingsCloseWidget(QtWidgets.QWidget):
    settings_clicked = QtCore.pyqtSignal()
    close_clicked = QtCore.pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/icons/settings.png")))
        self.settings_button.setIconSize(QtCore.QSize(15, 15))
        self.settings_button.setFlat(True)
        self.settings_button.setFixedSize(15, 15)

        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/icons/close.png")))
        self.close_button.setIconSize(QtCore.QSize(15, 15))
        self.close_button.setFlat(True)
        self.close_button.setFixedSize(15, 15)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.close_button)
        self.layout.setContentsMargins(5, 0, 0, 0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.settings_button.clicked.connect(self.settings_clicked.emit)
        self.close_button.clicked.connect(self.close_clicked.emit)
