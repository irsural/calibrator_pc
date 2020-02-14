from sqlite3 import Connection

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.on_run_edit_template_form import Ui_Dialog as OnRunEditConfigForm
from marks_widget import MarksWidget
from db_measures import MeasureParams, MeasureTables
import utils


class OnRunEditConfigDialog(QtWidgets.QDialog):
    def __init__(self, a_measure_config: MeasureParams, a_db_connection: Connection, a_db_tables: MeasureTables,
                 a_parent=None):

        super().__init__(a_parent)

        self.ui = OnRunEditConfigForm()
        self.ui.setupUi(self)

        self.measure_config = a_measure_config

        self.marks_widget = MarksWidget(a_db_connection, a_db_tables, a_default_mode=False, a_parent=self)
        self.ui.marks_widget_layout.addWidget(self.marks_widget)

        self.set_up_params_to_ui()

    def set_up_params_to_ui(self):
        self.ui.user_name_edit.setText(self.measure_config.user)
        self.ui.device_name_edit.setText(self.measure_config.device_name)
        self.ui.serial_number_edit.setText(self.measure_config.serial_num)
        self.ui.owner_edit.setText(self.measure_config.owner)
        self.ui.device_creator_edit.setText(self.measure_config.device_creator)
        self.ui.date_edit.setDate(QtCore.QDate.fromString(self.measure_config.date, "dd.MM.yyyy"))

        self.ui.organisation_edit.setText(self.measure_config.organisation)
        self.ui.system_combobox.setCurrentIndex(self.measure_config.device_system)
        self.ui.comment_edit.setText(self.measure_config.comment)

