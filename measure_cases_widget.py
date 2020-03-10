from typing import List

from PyQt5 import QtCore, QtWidgets, QtGui

from custom_widgets.EditListDialog import EditedListOnlyNumbers
from scale_limits_dialog import ScaleLimitsDialog
from MeasureView import MeasureView
from db_measures import Measure, MeasuresDB
import calibrator_constants as clb
import constants as cfg
import utils


class SettingsCloseWidget(QtWidgets.QWidget):
    settings_clicked = QtCore.pyqtSignal()
    close_clicked = QtCore.pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setIcon(QtGui.QIcon(QtGui.QPixmap(cfg.SETTINGS_ICON_PATH)))
        self.settings_button.setIconSize(QtCore.QSize(15, 15))
        self.settings_button.setFlat(True)
        self.settings_button.setFixedSize(15, 15)

        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setIcon(QtGui.QIcon(QtGui.QPixmap(cfg.CLOSE_ICON_PATH)))
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


class MeasureCases(QtWidgets.QWidget):
    case_added = QtCore.pyqtSignal()
    case_removed = QtCore.pyqtSignal(int)
    current_case_changed = QtCore.pyqtSignal(int)

    def __init__(self, a_measure_id, a_measures_db: MeasuresDB, a_case_table: QtWidgets.QTableView,
                 a_cases: List[Measure.Case], a_parent=None):
        super().__init__(a_parent)

        self.cases_bar = QtWidgets.QTabBar(self)
        self.cases_bar.setStyleSheet(
            "QTabBar::tab:last { margin-right: 2px; margin-left:0px; padding-left: 0; }\n"
            "QTabBar::tab:selected { background: white; border: 1px solid #000000; border-bottom: 0; }\n"
            "QTabBar::tab { padding-left: 6px; height: 30px }")
        self.set_up_tab_widget()

        assert a_cases, "Every measure must have at least 1 case!!!"
        self.measure_view = MeasureView(a_case_table, a_cases[0])

        self.parent = a_parent
        self.measures_db: MeasuresDB = a_measures_db
        self.measure_id = a_measure_id
        self.cases = a_cases

        for case in self.cases:
            self.add_new_tab(case)
        self.select_case(0)

    def __del__(self):
        print("measure cases deleted")

    def set_up_tab_widget(self):
        self.cases_bar.setExpanding(False)

        plus_button = QtWidgets.QPushButton("+")
        plus_button.setFlat(True)
        plus_button.setFixedSize(20, 20)
        self.cases_bar.addTab("")
        self.cases_bar.setTabEnabled(self.cases_bar.count() - 1, False)
        self.cases_bar.setTabButton(self.cases_bar.count() - 1, QtWidgets.QTabBar.RightSide, plus_button)
        # self.cases_bar.tabCloseRequested.connect(self.remove_tab)
        plus_button.clicked.connect(self.plus_button_clicked)

    def plus_button_clicked(self):
        self.add_new_tab()

    def select_case(self, a_idx):
        self.cases_bar.setCurrentIndex(a_idx)
        self.measure_view.reset(self.cases[a_idx])

    def add_new_tab(self, a_case: Measure.Case = None):
        try:
            new_tab_index = self.cases_bar.count() - 1

            if a_case is None:
                a_case = Measure.Case()
                # a_case = self.measures_db.new_case(self.measure_id, a_case)
                pass

            settings_close_widget = SettingsCloseWidget(self.cases_bar)
            settings_close_widget.setProperty("case_id", a_case.id)
            settings_close_widget.settings_clicked.connect(self.open_case_settings)
            settings_close_widget.close_clicked.connect(self.delete_case)

            self.cases_bar.insertTab(new_tab_index, self.create_tab_name(a_case))
            self.cases_bar.setTabButton(new_tab_index, QtWidgets.QTabBar.RightSide, settings_close_widget)

            self.cases_bar.setCurrentIndex(new_tab_index)
        except Exception as err:
            utils.exception_handler(err)

    def open_case_settings(self):
        sender = self.sender()
        case_id = int(sender.property("case_id"))
        print(case_id)

    def delete_case(self):
        sender = self.sender()
        case_id = int(sender.property("case_id"))
        print(case_id)

    def create_tab_name(self, a_case: Measure.Case):
        return " " + clb.enum_to_signal_type_short[a_case.signal_type] + "; " + \
               utils.value_to_user_with_units(clb.signal_type_to_units[a_case.signal_type])(a_case.limit)

    def remove_tab(self, a_idx: int):
        try:
            if self.cases_bar.count() > 2:
                tab_name = self.cases_bar.tabText(self.cases_bar.currentIndex())
                res = QtWidgets.QMessageBox.question(self, "Подтвердите действие",
                                                     f"Вы действительно хотите удалить измерение {tab_name}?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)
                if res == QtWidgets.QMessageBox.Yes:
                    if a_idx == self.cases_bar.count() - 2 and a_idx == self.cases_bar.currentIndex():
                        # Если удаляемая вкладка активна, меняем активную на предыдущую
                        self.cases_bar.setCurrentIndex(self.cases_bar.count() - 3)
                    # self.measures_db.delete_case(self.measure_id, self.get_tab_case_id(a_idx))
                    self.cases_bar.removeTab(a_idx)
                    self.cases.pop(a_idx)

        except Exception as err:
            utils.exception_handler(err)

    def edit_scale_limits(self):
        try:
            case_id = self.get_tab_case_id(self.cases_bar.currentIndex())
            case: Measure.Case = self.measure_db.get_case(case_id)

            case_params_dialog = CaseParamsDialog(case, self)

            new_case_params = case_params_dialog.exec_and_get_limits()
            if new_case_params is not None:
                self.measures_db.update_case(case)
        except Exception as err:
            utils.exception_handler(err)

    def get_tab_case_id(self, a_tab_idx: int):
        return self.cases_bar.tabButton(a_tab_idx, QtWidgets.QTabBar.RightSide).property("case_id")

    def current_case(self):
        return self.cases[self.cases_bar.currentIndex()]

    # def get_scales(self) -> List[cfg.Scale]:
    #     scales = [self.get_scale_by_tab_idx(tab_idx) for tab_idx in range(self.cases_bar.count() - 1)]
    #     return scales

    # def get_scale_by_tab_idx(self, a_tab_idx):
    #     scale_points_list: EditedListOnlyNumbers = self.ui.measure_cases_tabwidget.widget(a_tab_idx)
    #     scale_number = a_tab_idx + 1
    #     Пределы обновляются в базе сразу после изменения, их передавать не нужно
        # return cfg.Scale(a_id=self.scales_id[scale_number], a_number=scale_number,
        #                  a_scale_points=scale_points_list.get_list())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = SettingsCloseWidget()
    w.show()
    sys.exit(app.exec())
