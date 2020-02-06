from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.template_list_form_2 import Ui_Dialog as TemplateListForm
from variable_template_fields_dialog import VariableTemplateFieldsDialog, VariableTemplateParams
import utils


class TemplateParams:
    def __init__(self, a_name = "Новый шаблон"):
        self.name = a_name


class TemplateListWindow(QtWidgets.QDialog):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = TemplateListForm()
        self.ui.setupUi(self)
        self.ui.template_params_widget.setDisabled(True)
        self.show()

        self.ui.choose_template_button.clicked.connect(self.choose_template)
        self.ui.templates_list.itemDoubleClicked.connect(self.choose_template)

        self.ui.save_template_button.clicked.connect(self.save_template)
        self.ui.cancel_edit_template_button.clicked.connect(self.cancel_template_edit)

        self.ui.templates_list.customContextMenuRequested.connect(self.show_context_menu)

        self.ui.show_template_details_button.clicked.connect(self.ui.template_params_widget.hide)

    @pyqtSlot(QtCore.QPoint)
    def show_context_menu(self, a_pos: QtCore.QPoint):
        menu = QtWidgets.QMenu()
        menu.addAction("Новый шаблон", self.create_new_template)

        template_chosen: bool = self.ui.templates_list.currentRow() != -1
        duplicate_act = menu.addAction("Дублировать", self.duplicate_template)
        duplicate_act.setEnabled(template_chosen)

        edit_act = menu.addAction("Редактировать", self.edit_template)
        edit_act.setEnabled(template_chosen)
        delete_act = menu.addAction("Удалить", self.delete_template)
        delete_act.setEnabled(template_chosen)

        global_pos = self.ui.templates_list.mapToGlobal(a_pos)
        menu.exec(global_pos)

    def activate_edit_template(self):
        self.ui.template_params_widget.setDisabled(False)
        self.ui.choose_templates_widget.setDisabled(True)

    @pyqtSlot()
    def activate_choose_template(self):
        self.ui.template_params_widget.setDisabled(True)
        self.ui.choose_templates_widget.setDisabled(False)

    @pyqtSlot()
    def choose_template(self):
        item = self.ui.templates_list.currentItem()
        if item is not None:
            # Показать переменные параметры
            variable_params_dialog = VariableTemplateFieldsDialog()
            params: VariableTemplateParams = variable_params_dialog.exec_and_get_params()
            if params is not None:
                print(params.serial_num, params.date)


    @pyqtSlot()
    def create_new_template(self, a_template_params=TemplateParams()):
        QtWidgets.QListWidgetItem(a_template_params.name, self.ui.templates_list)

    @pyqtSlot()
    def duplicate_template(self):
        current_template = self.ui.templates_list.currentItem()
        source_template_params = TemplateParams(current_template.text())
        self.create_new_template(source_template_params)

    @pyqtSlot()
    def edit_template(self):
        self.activate_edit_template()

    @pyqtSlot()
    def save_template(self):
        self.activate_choose_template()

    @pyqtSlot()
    def cancel_template_edit(self):
        self.activate_choose_template()

    @pyqtSlot()
    def delete_template(self):
        self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
