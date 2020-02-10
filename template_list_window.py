from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui.py.template_list_form import Ui_Dialog as TemplateListForm
from variable_template_fields_dialog import VariableTemplateFieldsDialog, VariableTemplateParams
from db_templates import TemplateParams, TemplatesDB
from constants import OperationDB
import qt_utils
import utils


class TemplateListWindow(QtWidgets.QDialog):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = TemplateListForm()
        self.ui.setupUi(self)
        self.ui.template_params_widget.setDisabled(True)

        self.db_operation = OperationDB.ADD
        self.prev_template_name = ""
        self.templates_db = TemplatesDB("templates.db")

        self.current_template = None
        for params in self.templates_db:
            QtWidgets.QListWidgetItem(params.name, self.ui.templates_list)

        self.ui.choose_template_button.clicked.connect(self.choose_template)
        self.ui.templates_list.itemDoubleClicked.connect(self.choose_template)

        self.ui.save_template_button.clicked.connect(self.save_template)
        self.ui.cancel_edit_template_button.clicked.connect(self.cancel_template_edit)

        self.ui.templates_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.templates_list.itemClicked.connect(self.template_changed)

        self.ui.template_name_edit.textChanged.connect(self.template_name_changed)

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
        delete_act = menu.addAction("Удалить", self.delete_current_template)
        delete_act.setEnabled(template_chosen)

        global_pos = self.ui.templates_list.mapToGlobal(a_pos)
        menu.exec(global_pos)

    @pyqtSlot(str)
    def template_name_changed(self, new_template_name: str):
        self.current_template.name = new_template_name
        self.ui.templates_list.currentItem().setText(new_template_name)

    def activate_edit_template(self):
        self.ui.template_params_widget.setDisabled(False)
        self.ui.choose_templates_widget.setDisabled(True)

    @pyqtSlot()
    def activate_choose_template(self):
        self.ui.template_params_widget.setDisabled(True)
        self.ui.choose_templates_widget.setDisabled(False)

    @pyqtSlot(QtWidgets.QListWidgetItem)
    def template_changed(self, a_current: QtWidgets.QListWidgetItem):
        try:
            if a_current is not None:
                self.current_template: TemplateParams = self.templates_db.get(a_current.text())
                assert self.current_template is not None, "database operation 'get' has failed!"
                self.fill_template_info_to_ui(self.current_template)
        except AssertionError as err:
            print(err)

    def fill_template_info_to_ui(self, a_template_params):
        self.ui.template_name_edit.setText(a_template_params.name)
        self.ui.organisation_edit.setText(a_template_params.organisation)
        self.ui.etalon_device_edit.setText(a_template_params.etalon_device)
        self.ui.device_name_edit.setText(a_template_params.device_name)
        self.ui.device_creator_edit.setText(a_template_params.device_creator)

        self.ui.device_system_combobox.setCurrentIndex(a_template_params.device_system)
        self.ui.signal_type_combobox.setCurrentIndex(a_template_params.signal_type)
        self.ui.class_spinbox.setValue(a_template_params.device_class)

        qt_utils.qtablewidget_clear(self.ui.points_table)
        for point in a_template_params.points:
            qt_utils.qtablewidget_append_row(self.ui.points_table, point)

    def fill_template_info_to_db(self):
        self.current_template.organisation = self.ui.organisation_edit.text()
        self.current_template.etalon_device = self.ui.etalon_device_edit.text()
        self.current_template.device_name = self.ui.device_name_edit.text()
        self.current_template.device_creator = self.ui.device_creator_edit.text()
        self.current_template.device_system = self.ui.device_system_combobox.currentIndex()
        self.current_template.signal_type = self.ui.signal_type_combobox.currentIndex()
        self.current_template.device_class = self.ui.class_spinbox.value()

    @pyqtSlot()
    def create_new_template(self, a_template_params=None):
        if a_template_params is None:
            a_template_params = TemplateParams(a_name="Новый шаблон", a_device_name="Калибратор N4-25")
        self.current_template = a_template_params

        copy_number = 0
        source_template_name = str(a_template_params.name)
        while self.templates_db.is_name_exist(a_template_params.name):
            copy_number += 1
            a_template_params.name = f"{source_template_name}_{copy_number}"

        new_item = QtWidgets.QListWidgetItem(a_template_params.name, self.ui.templates_list)
        self.ui.templates_list.setCurrentItem(new_item)
        self.fill_template_info_to_ui(self.current_template)
        self.db_operation = OperationDB.ADD
        self.activate_edit_template()

    @pyqtSlot()
    def duplicate_template(self):
        try:
            current_template_name = self.ui.templates_list.currentItem().text()
            duplicate_template = self.templates_db.get(current_template_name)
            assert duplicate_template is not None, "database operation 'get' has failed!"

            self.create_new_template(duplicate_template)
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def edit_template(self):
        self.db_operation = OperationDB.EDIT
        self.prev_template_name = self.current_template.name
        self.activate_edit_template()

    @pyqtSlot()
    def save_template(self):
        try:
            self.fill_template_info_to_db()
            if self.db_operation == OperationDB.ADD:
                result = self.templates_db.add(self.current_template)
            else:
                result = self.templates_db.edit(self.prev_template_name, self.current_template)

            if result:
                self.activate_choose_template()
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка сохранения шаблона",
                                               "Шаблон с таким именем уже существует!", QtWidgets.QMessageBox.Ok)
        except Exception as err:
            print(err)

    @pyqtSlot()
    def cancel_template_edit(self):
        self.activate_choose_template()
        if self.db_operation == OperationDB.ADD:
            self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
        else:
            # Восстанавливаем значения в полях
            self.current_template.name = self.prev_template_name
            self.fill_template_info_to_ui(self.current_template)

    @pyqtSlot()
    def delete_current_template(self):
        try:
            deleted_item = self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
            result = self.templates_db.delete(deleted_item.text())
            assert result, "database operation 'delete' has failed!"
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def choose_template(self):
        item = self.ui.templates_list.currentItem()
        if item is not None:
            variable_params_dialog = VariableTemplateFieldsDialog()
            params: VariableTemplateParams = variable_params_dialog.exec_and_get_params()
            if params is not None:
                print(params.serial_num, params.date)
                # Здесь начинаем измерение

