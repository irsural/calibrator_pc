from PyQt5 import QtCore, QtWidgets

from ui.py.variable_template_fields_form import Ui_variable_template_fields_dialog as VariableTemplateFieldsForm


class VariableTemplateParams:
    def __init__(self, a_serial_num="", a_owner="", a_user_name="", a_date=""):
        self.serial_num = a_serial_num
        self.owner = a_owner
        self.user_name = a_user_name
        self.date = a_date
        self.time = QtCore.QTime.currentTime().toString("H:mm")


class VariableTemplateFieldsDialog(QtWidgets.QDialog):
    def __init__(self, a_parent=None, a_variable_params=None):
        super().__init__(a_parent)

        self.ui = VariableTemplateFieldsForm()
        self.ui.setupUi(self)

        self.variable_params = a_variable_params if a_variable_params is not None else VariableTemplateParams()
        self.recover_params(self.variable_params)

        self.ui.accept_button.clicked.connect(self.accept)
        self.ui.reject_button.clicked.connect(self.reject)

    def __del__(self):
        print("variable deleted")

    def recover_params(self, a_params):
        self.ui.serial_number_edit.setText(a_params.serial_num)
        self.ui.owner_edit.setText(a_params.owner)
        self.ui.user_name_edit.setText(a_params.user_name)
        self.ui.date_edit.setDate(QtCore.QDate.currentDate())

    def extract_params(self) -> VariableTemplateParams:
        return VariableTemplateParams(a_serial_num=self.ui.serial_number_edit.text(),
                                      a_owner=self.ui.owner_edit.text(),
                                      a_user_name=self.ui.user_name_edit.text(),
                                      a_date=self.ui.date_edit.text())

    def exec_and_get_params(self):
        if self.exec() == QtWidgets.QDialog.Accepted:
            return self.extract_params()
        else:
            return None
