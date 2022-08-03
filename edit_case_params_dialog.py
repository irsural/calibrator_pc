from PyQt5 import QtCore, QtWidgets

from ui.py.edit_case_params_form import Ui_edit_case_params_dialog as EditCaseParamsForm
from db_measures import Measure
import irspy.clb.calibrator_constants as clb
from irspy.qt import qt_utils
from irspy import utils


class EditCaseParamsDialog(QtWidgets.QDialog):
    def __init__(self, a_case: Measure.Case, a_parent=None):
        super().__init__(a_parent)

        self.ui = EditCaseParamsForm()
        self.ui.setupUi(self)
        self.ui.default_button.hide()

        self.case = a_case

        self.recover_params()

        self.ui.limit_edit.textEdited.connect(self.edit_text_edited)
        self.ui.limit_edit.editingFinished.connect(self.editing_finished)

        self.ui.minimal_discrete_edit.textEdited.connect(self.edit_text_edited)
        self.ui.minimal_discrete_edit.editingFinished.connect(self.editing_finished)

        self.ui.signal_type_combobox.currentIndexChanged.connect(self.signal_type_changed)

        self.ui.accept_button.clicked.connect(self.save_params)
        self.ui.reject_button.clicked.connect(self.reject)

    def __del__(self):
        print("EditCaseParamsDialog deleted")

    def edit_text_edited(self):
        try:
            edit = self.sender()
            assert isinstance(edit, QtWidgets.QLineEdit), "edit_text_edited must be connected to QLineEdit event!"

            self.update_edit_color(edit)
        except AssertionError as err:
            print(err)

    @staticmethod
    def update_edit_color(a_edit: QtWidgets.QLineEdit):
        try:
            utils.parse_input(a_edit.text())
            a_edit.setStyleSheet(qt_utils.QSTYLE_COLOR_WHITE)
        except ValueError:
            a_edit.setStyleSheet(qt_utils.QSTYLE_COLOR_RED)

    def editing_finished(self):
        try:
            edit = self.sender()
            assert isinstance(edit, QtWidgets.QLineEdit), "editinig_finished must be connected to QLineEdit event!"
            self.normalize_edit_value(edit)
        except AssertionError as err:
            print(err)

    def normalize_edit_value(self, edit: QtWidgets.QLineEdit):
        try:
            value = utils.parse_input(edit.text())
            value = clb.bound_amplitude(value, self.case.signal_type)
            edit.setText(utils.value_to_user_with_units(clb.signal_type_to_units[self.case.signal_type])(value))
            self.update_edit_color(edit)
        except ValueError:
            pass

    def signal_type_changed(self, a_signal_type: int):
        self.case.signal_type = clb.SignalType(a_signal_type)
        self.normalize_edit_value(self.ui.limit_edit)
        self.normalize_edit_value(self.ui.minimal_discrete_edit)

    def recover_params(self):
        self.ui.limit_edit.setText(utils.value_to_user_with_units(
            clb.signal_type_to_units[self.case.signal_type])(self.case.limit))

        self.ui.minimal_discrete_edit.setText(utils.value_to_user_with_units(
            clb.signal_type_to_units[self.case.signal_type])(self.case.minimal_discrete))

        self.ui.signal_type_combobox.setCurrentIndex(self.case.signal_type)
        self.ui.device_class_spinbox.setValue(self.case.device_class)

    def save_params(self):
        limit = utils.parse_input(self.ui.limit_edit.text())
        if limit != 0:
            if self.case.limit != limit:
                # Это сбрасывает точки шкалы в таблице
                self.case.scale_coef = 0

            self.case.limit = limit
            self.case.minimal_discrete = utils.parse_input(self.ui.minimal_discrete_edit.text())
            self.case.signal_type = clb.SignalType(self.ui.signal_type_combobox.currentIndex())
            self.case.device_class = self.ui.device_class_spinbox.value()

            self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Предел не может быть равен нулю",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
