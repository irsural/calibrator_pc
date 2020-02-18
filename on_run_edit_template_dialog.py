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

        assert a_measure_config.id != 0, "Measure id must not be zero!"
        self.marks_widget = MarksWidget(a_db_connection, a_db_tables, a_measure_id=self.measure_config.id,
                                        a_parent=self)
        self.ui.marks_widget_layout.addWidget(self.marks_widget)

        self.set_up_params_to_ui()

        self.ui.accept_button.clicked.connect(self.save_pressed)
        self.ui.reject_button.clicked.connect(self.reject)

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

    def save_pressed(self):
        if self.marks_widget.save():
            self.save()
            self.close()

    def save(self):
        self.measure_config.user = self.ui.user_name_edit.text()
        self.measure_config.device_name = self.ui.device_name_edit.text()
        self.measure_config.serial_num = self.ui.serial_number_edit.text()
        self.measure_config.owner = self.ui.owner_edit.text()
        self.measure_config.device_creator = self.ui.device_creator_edit.text()
        self.measure_config.date = self.ui.date_edit.text()
        self.measure_config.organisation = self.ui.organisation_edit.text()
        self.measure_config.device_system = self.ui.system_combobox.currentIndex()
        self.measure_config.comment = self.ui.comment_edit.text()

