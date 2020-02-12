from enum import IntEnum
from sqlite3 import Connection

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.settings_form import Ui_Dialog as SettingsForm
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

    def __init__(self, a_db_connection: Connection, a_marks_table_name: str, a_parent=None):
        super().__init__(a_parent)

        self.ui = SettingsForm()
        self.ui.setupUi(self)

        self.window_existing_timer = QtCore.QTimer()
        self.window_existing_timer.timeout.connect(self.window_existing_chech)
        self.window_existing_timer.start(3000)

        self.marks_widget = MarksWidget(a_db_connection, a_marks_table_name, a_default_mode=True, a_parent=self)
        marks_layout = QtWidgets.QGridLayout(self)
        marks_layout.addWidget(self.marks_widget)
        marks_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.marks_page.setLayout(marks_layout)

    def window_existing_chech(self):
        print("Settings Dialog")

    # def change_settings_widget(self):
    #     current_widget

    def save(self):
        pass

    def save_and_exit(self):
        self.save()
        self.close()

