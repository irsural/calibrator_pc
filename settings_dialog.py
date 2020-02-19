from enum import IntEnum
from sqlite3 import Connection

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from custom_widgets.EditListDialog import EditedListWithUnits
from ui.py.settings_form import Ui_Dialog as SettingsForm
from settings_ini_parser import Settings
from db_measures import MeasureTables
from marks_widget import MarksWidget
import calibrator_constants as clb
import qt_utils
import utils


class SettingsDialog(QtWidgets.QDialog):
    class SettingPages:
        MARKS = 0
        FIXED_RANGE = 1

    page_num_to_widget = {
        SettingPages.MARKS: MarksWidget,
        SettingPages.FIXED_RANGE: None
    }

    fixed_range_changed = pyqtSignal()

    def __init__(self, a_settings: Settings, a_db_connection: Connection, a_db_tables: MeasureTables,
                 a_parent=None):
        super().__init__(a_parent)

        self.ui = SettingsForm()
        self.ui.setupUi(self)

        self.settings = a_settings

        self.ui.save_and_exit_button.clicked.connect(self.save_and_exit)
        self.ui.save_button.clicked.connect(self.save)
        self.ui.cancel_button.clicked.connect(self.close)

        self.marks_widget = MarksWidget(a_db_connection, a_db_tables, a_parent=self)
        self.ui.marks_layout.addWidget(self.marks_widget)

        self.edit_fixed_range_widget = EditedListWithUnits(self, "В", (), a_list_name="Шаг")
        self.ui.fixed_range_groupbox.layout().addWidget(self.edit_fixed_range_widget)

        self.ui.settings_menu_list.setCurrentRow(0)
        self.ui.settings_stackedwidget.setCurrentIndex(0)

    def save(self):
        try:
            return self.marks_widget.save()
        except Exception as err:
            print(err)

    def save_and_exit(self):
        if self.save():
            self.close()

