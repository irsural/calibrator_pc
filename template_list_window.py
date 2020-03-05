from enum import IntEnum

from PyQt5 import QtCore, QtGui, QtWidgets

from variable_template_fields_dialog import VariableTemplateFieldsDialog, VariableTemplateParams
from ui.py.template_list_form import Ui_Dialog as TemplateListForm
from custom_widgets.QTableDelegates import TableEditDoubleClick
from template_scales_widget import ScalesWidget
from db_templates import TemplateParams, TemplatesDB
from constants import OperationDB, MeasuredPoint
from settings_ini_parser import Settings
import calibrator_constants as clb
import qt_utils
import utils


class TemplateListWindow(QtWidgets.QDialog):
    config_ready = QtCore.pyqtSignal(TemplateParams, VariableTemplateParams)

    def __init__(self, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = TemplateListForm()
        self.ui.setupUi(self)
        self.ui.template_params_widget.setDisabled(True)

        # parent не передается намеренно, иначе scales_widget не удаляется из за чего не удаяется parent
        self.scales_widget = ScalesWidget()
        self.ui.scales_layout.addWidget(self.scales_widget)

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        self.templates_db = TemplatesDB("templates.db")

        self.current_template: TemplateParams = TemplateParams()
        # for template_id, name in self.templates_db:
        for template_id, name in self.templates_db:
            list_item = QtWidgets.QListWidgetItem(name)
            list_item.setData(QtCore.Qt.UserRole, template_id)
            self.ui.templates_list.addItem(list_item)

        self.ui.add_template_button.clicked.connect(self.add_template_clicked)
        self.ui.edit_template_button.clicked.connect(self.edit_template)
        self.ui.duplicate_template_button.clicked.connect(self.duplicate_template)
        self.ui.delete_template_button.clicked.connect(self.delete_current_template)

        self.ui.choose_template_button.clicked.connect(self.choose_template)
        self.ui.templates_list.itemDoubleClicked.connect(self.choose_template)

        self.ui.save_template_button.clicked.connect(self.save_template)
        self.ui.cancel_edit_template_button.clicked.connect(self.cancel_template_edit)

        self.ui.templates_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.templates_list.currentItemChanged.connect(self.template_changed)

        self.ui.template_name_edit.textChanged.connect(self.template_name_changed)
        self.ui.filter_edit.textChanged.connect(self.filter_templates)

        self.ui.templates_list.setCurrentRow(0)

    def __del__(self):
        print("templates list deleted")

    def show_context_menu(self, a_pos: QtCore.QPoint):
        menu = QtWidgets.QMenu()
        menu.addAction("Новый шаблон", self.add_template_clicked)

        template_chosen: bool = self.ui.templates_list.currentRow() != -1
        duplicate_act = menu.addAction("Дублировать", self.duplicate_template)
        duplicate_act.setEnabled(template_chosen)

        edit_act = menu.addAction("Редактировать", self.edit_template)
        edit_act.setEnabled(template_chosen)
        delete_act = menu.addAction("Удалить", self.delete_current_template)
        delete_act.setEnabled(template_chosen)

        global_pos = self.ui.templates_list.mapToGlobal(a_pos)
        menu.exec(global_pos)

    def template_name_changed(self, new_template_name: str):
        self.current_template.name = new_template_name
        self.ui.templates_list.currentItem().setText(new_template_name)

    def activate_edit_template(self):
        self.ui.template_params_widget.setDisabled(False)
        self.ui.choose_templates_widget.setDisabled(True)

    def activate_choose_template(self):
        self.ui.template_params_widget.setDisabled(True)
        self.ui.choose_templates_widget.setDisabled(False)

    def template_changed(self, a_current: QtWidgets.QListWidgetItem):
        try:
            if a_current is not None:
                self.current_template: TemplateParams = self.templates_db.get(a_current.data(QtCore.Qt.UserRole))
                assert self.current_template is not None, "database operation 'get' has failed!"
                self.fill_template_info_to_ui(self.current_template)
        except AssertionError as err:
            print(err)

    def fill_template_info_to_ui(self, a_template_params: TemplateParams):
        self.ui.template_name_edit.setText(a_template_params.name)
        self.ui.device_name_edit.setText(a_template_params.device_name)
        self.ui.device_creator_edit.setText(a_template_params.device_creator)
        self.ui.device_system_combobox.setCurrentIndex(a_template_params.device_system)

        for scale in a_template_params.scales:
            self.scales_widget.append_scale(scale)

    def add_template_clicked(self):
        self.create_new_template()

    def create_new_template(self, a_template_params=None):
        self.current_template = a_template_params if \
            a_template_params is not None else TemplateParams(a_name="Новый шаблон")

        copy_number = 0
        source_template_name = self.current_template.name
        while self.templates_db.is_name_exist(self.current_template.name):
            copy_number += 1
            self.current_template.name = f"{source_template_name}_{copy_number}"

        new_id = self.templates_db.new(self.current_template)
        self.current_template.id = new_id

        new_item = QtWidgets.QListWidgetItem(self.current_template.name, self.ui.templates_list)
        new_item.setData(QtCore.Qt.UserRole, self.current_template.id)

        self.ui.templates_list.setCurrentItem(new_item)

        self.activate_edit_template()

    def duplicate_template(self):
        try:
            current_template_id: int = self.ui.templates_list.currentItem().data(QtCore.Qt.UserRole)
            duplicate_template = self.templates_db.get(current_template_id)
            assert duplicate_template is not None, "database operation 'get' has failed!"

            self.create_new_template(duplicate_template)
        except AssertionError as err:
            print(err)

    def edit_template(self):
        if self.ui.templates_list.selectedItems():
            self.activate_edit_template()

    def save_template(self):
        self.current_template.device_name = self.ui.device_name_edit.text()
        self.current_template.device_creator = self.ui.device_creator_edit.text()
        self.current_template.device_system = self.ui.device_system_combobox.currentIndex()

        self.templates_db.save(self.current_template)

        self.activate_choose_template()

    def cancel_template_edit(self):
        self.templates_db.cancel()

        self.activate_choose_template()

        if not self.templates_db.is_id_exist(self.current_template.id):
            self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
        else:
            self.template_changed(self.ui.templates_list.currentItem())

    def delete_current_template(self):
        try:
            deleted_item = self.ui.templates_list.currentItem()
            deleted_id: int = deleted_item.data(QtCore.Qt.UserRole)
            reply = QtWidgets.QMessageBox.question(self, "Подтвердите действие", f"Вы действительно хотите удалить "
                                                   f"шаблон '{deleted_item.text()}'?", QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
                self.templates_db.delete(deleted_id)
        except Exception as err:
            print(err)

    def choose_template(self):
        try:
            item = self.ui.templates_list.currentItem()
            if item is not None:
                variable_params_dialog = VariableTemplateFieldsDialog(self)
                params: VariableTemplateParams = variable_params_dialog.exec_and_get_params()
                if params is not None:
                    self.config_ready.emit(self.current_template, params)
                    self.reject()
        except Exception as err:
            utils.exception_handler(err)

    def filter_templates(self, a_text):
        for row in range(self.ui.templates_list.count()):
            item = self.ui.templates_list.item(row)
            item.setHidden(a_text.lower() not in item.text().lower())

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        self.scales_widget.close()
        a_event.accept()
