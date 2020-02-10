from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.variable_template_fields_form import Ui_Dialog as VariableTemplateFieldsForm
import utils


class VariableTemplateParams:
    def __init__(self, a_serial_num="", a_owner="", a_user_name="", a_date="", a_temperature="", a_wet="",
                 a_pressure="", a_warming_time=""):
        self.serial_num = a_serial_num
        self.owner = a_owner
        self.user_name = a_user_name
        self.date = a_date
        self.temperature = a_temperature
        self.wet = a_wet
        self.pressure = a_pressure
        self.warming_time = a_warming_time


class VariableTemplateFieldsDialog(QtWidgets.QDialog):
    def __init__(self, a_parent=None, a_variable_params=VariableTemplateParams()):
        super().__init__(a_parent)

        self.ui = VariableTemplateFieldsForm()
        self.ui.setupUi(self)

        self.variable_params = a_variable_params
        self.recover_params(self.variable_params)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.reject_button.clicked.connect(self.reject)

    def recover_params(self, a_params):
        self.ui.serial_number_edit.setText(a_params.serial_num)
        self.ui.owner_edit.setText(a_params.owner)
        self.ui.user_name_edit.setText(a_params.user_name)
        self.ui.date_edit.setDate(QtCore.QDate.currentDate())
        self.ui.temperature_edit.setText(a_params.temperature)
        self.ui.wet_edit.setText(a_params.wet)
        self.ui.pressure_edit.setText(a_params.pressure)
        self.ui.warming_up_time_edit.setText(a_params.warming_time)

    def extract_params(self) -> VariableTemplateParams:
        return VariableTemplateParams(a_serial_num=self.ui.serial_number_edit.text(),
                                      a_owner=self.ui.owner_edit.text(),
                                      a_user_name=self.ui.user_name_edit.text(),
                                      a_date=self.ui.date_edit.text(),
                                      a_temperature=self.ui.temperature_edit.text(),
                                      a_wet=self.ui.wet_edit.text(),
                                      a_pressure=self.ui.pressure_edit.text(),
                                      a_warming_time=self.ui.warming_up_time_edit.text())

    def exec_and_get_params(self):
        if self.exec() == QtWidgets.QDialog.Accepted:
            return self.extract_params()
        else:
            return None

