from sqlite3 import Connection

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from irspy.qt.custom_widgets.EditListDialog import EditedListWithUnits
from ui.py.settings_form import Ui_settings_dialog as SettingsForm
from irspy.qt.qt_settings_ini_parser import QtSettings
from marks_widget import MarksWidget
import irspy.clb.calibrator_constants as clb


class SettingsDialog(QtWidgets.QDialog):
    class SettingPages:
        MARKS = 0
        FIXED_RANGE = 1

    page_num_to_widget = {
        SettingPages.MARKS: MarksWidget,
        SettingPages.FIXED_RANGE: None
    }

    fixed_range_changed = pyqtSignal()

    def __init__(self, a_settings: QtSettings, a_db_connection: Connection, a_parent=None):
        super().__init__(a_parent)

        self.ui = SettingsForm()
        self.ui.setupUi(self)

        self.settings = a_settings
        self.settings.restore_qwidget_state(self)

        self.ui.save_and_exit_button.clicked.connect(self.save_and_exit)
        self.ui.save_button.clicked.connect(self.save)
        self.ui.cancel_button.clicked.connect(self.close)

        self.marks_widget = MarksWidget(self.__class__.__name__, self.settings, a_db_connection,
                                        a_parent=None)
        self.ui.marks_layout.addWidget(self.marks_widget)

        self.edit_fixed_range_widget = EditedListWithUnits(
            self, "В", self.settings.fixed_step_list, clb.MIN_VOLTAGE, clb.MAX_VOLTAGE,
            a_optional_widget=QtWidgets.QLabel("Шаг", self))
        self.ui.fixed_range_groupbox.layout().addWidget(self.edit_fixed_range_widget)

        self.ui.exact_step_spinbox.setValue(self.settings.exact_step)
        self.ui.rough_step_spinbox.setValue(self.settings.rough_step)
        self.ui.common_step_spinbox.setValue(self.settings.common_step)
        self.ui.start_deviation_spinbox.setValue(self.settings.start_deviation)
        self.ui.mouse_inversion_checkbox.setChecked(self.settings.mouse_inversion)
        self.ui.disable_scroll_on_table_checkbox.setChecked(self.settings.disable_scroll_on_table)

        self.open_marks_table_widget()

    def __del__(self):
        print("settings deleted")

    def open_marks_table_widget(self):
        self.ui.settings_menu_list.setCurrentRow(0)
        self.ui.settings_stackedwidget.setCurrentIndex(0)

    def save(self):
        try:
            fixed_step_list = self.edit_fixed_range_widget.sort_list()
            if self.settings.fixed_step_list != fixed_step_list:
                self.settings.fixed_step_list = fixed_step_list

            if self.settings.rough_step != self.ui.rough_step_spinbox.value():
                self.settings.rough_step = self.ui.rough_step_spinbox.value()

            if self.settings.common_step != self.ui.common_step_spinbox.value():
                self.settings.common_step = self.ui.common_step_spinbox.value()

            if self.settings.exact_step != self.ui.exact_step_spinbox.value():
                self.settings.exact_step = self.ui.exact_step_spinbox.value()

            if self.settings.start_deviation != self.ui.start_deviation_spinbox.value():
                self.settings.start_deviation = self.ui.start_deviation_spinbox.value()

            if self.settings.mouse_inversion != int(self.ui.mouse_inversion_checkbox.isChecked()):
                self.settings.mouse_inversion = int(self.ui.mouse_inversion_checkbox.isChecked())

            if self.settings.disable_scroll_on_table != int(self.ui.disable_scroll_on_table_checkbox.isChecked()):
                self.settings.disable_scroll_on_table = int(self.ui.disable_scroll_on_table_checkbox.isChecked())

            if self.marks_widget.save():
                return True
            else:
                self.open_marks_table_widget()
                return False
        except Exception as err:
            print(err)

    def save_and_exit(self):
        if self.save():
            self.close()

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_qwidget_state(self)
        # Вызывается вручную, чтобы marks_widget сохранил состояние своего хэдера
        self.marks_widget.close()
        a_event.accept()
