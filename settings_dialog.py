from enum import IntEnum
from sqlite3 import Connection
import configparser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.settings_form import Ui_Dialog as SettingsForm
from custom_widgets.EditListDialog import EditedListWidget
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

    def __init__(self, a_settings: configparser.ConfigParser, a_db_connection: Connection, a_db_tables: MeasureTables,
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

        self.edit_fixed_range_widget = EditedListWidget(self, (), a_list_name="")
        self.ui.fixed_range_groupbox.layout().addWidget(self.edit_fixed_range_widget)

    def save(self):
        try:
            return self.marks_widget.save()
        except Exception as err:
            print(err)

    def save_and_exit(self):
        if self.save():
            self.close()

