from enum import IntEnum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from variable_template_fields_dialog import VariableTemplateFieldsDialog, VariableTemplateParams
from ui.py.template_list_form import Ui_Dialog as TemplateListForm
from custom_widgets.QTableDelegates import TableEditDoubleClick
from db_templates import TemplateParams, TemplatesDB
from settings_ini_parser import Settings
import calibrator_constants as clb
from constants import OperationDB, Point
import qt_utils
import utils


class TemplateListWindow(QtWidgets.QDialog):
    config_ready = pyqtSignal(TemplateParams, VariableTemplateParams)

    def __init__(self, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = TemplateListForm()
        self.ui.setupUi(self)
        self.ui.template_params_widget.setDisabled(True)

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        self.db_operation = OperationDB.ADD
        self.prev_template_name = ""
        self.templates_db = TemplatesDB("templates.db")

        self.current_template = TemplateParams()
        for name in self.templates_db:
            self.ui.templates_list.addItem(name)

        self.points_table = PointsDataTable(self.ui.signal_type_combobox.currentIndex(), self.ui.points_table)
        self.points_table.restore_header_state(self.settings.get_last_header_state(self.__class__.__name__))

        self.ui.signal_type_combobox.currentIndexChanged.connect(self.points_table.set_signal_type)
        self.ui.add_point_button.clicked.connect(self.points_table.append_point)
        self.ui.remove_point_button.clicked.connect(self.points_table.delete_selected_points)

        self.ui.add_template_button.clicked.connect(self.create_new_template)
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

    def __del__(self):
        print("templates list deleted")

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

        self.points_table.reset(a_template_params.points)

    # noinspection DuplicatedCode
    def fill_template_info_to_db(self):
        self.current_template.organisation = self.ui.organisation_edit.text()
        self.current_template.etalon_device = self.ui.etalon_device_edit.text()
        self.current_template.device_name = self.ui.device_name_edit.text()
        self.current_template.device_creator = self.ui.device_creator_edit.text()
        self.current_template.device_system = self.ui.device_system_combobox.currentIndex()
        self.current_template.signal_type = self.ui.signal_type_combobox.currentIndex()
        self.current_template.device_class = self.ui.class_spinbox.value()

        self.current_template.points = self.points_table.get_points()

    @pyqtSlot()
    def create_new_template(self, a_template_params=None):
        self.ui.templates_list.blockSignals(True)
        if a_template_params is None:
            a_template_params = TemplateParams(a_name="Новый шаблон", a_etalon_device="Калибратор N4-25")
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
        self.ui.templates_list.blockSignals(False)

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

        self.points_table.clear_points_edited_state()

    @pyqtSlot()
    def save_template(self):
        try:
            self.fill_template_info_to_db()
            if self.db_operation == OperationDB.ADD:
                result = self.templates_db.add(self.current_template)
            else:
                result = self.templates_db.edit(self.prev_template_name, self.current_template,
                                                self.points_table.were_points_edited())

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
        self.template_changed(self.ui.templates_list.currentItem())

    @pyqtSlot()
    def delete_current_template(self):
        try:
            deleted_item = self.ui.templates_list.currentItem()
            reply = QtWidgets.QMessageBox.question(self, "Подтвердите действие", f"Вы действительно хотите удалить "
                                                   f"шаблон '{deleted_item.text()}'?", QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.templates_list.takeItem(self.ui.templates_list.currentRow())
                result = self.templates_db.delete(deleted_item.text())
                assert result, "database operation 'delete' has failed!"
        except AssertionError as err:
            print(err)

    @pyqtSlot()
    def choose_template(self):
        item = self.ui.templates_list.currentItem()
        if item is not None:
            variable_params_dialog = VariableTemplateFieldsDialog(self)
            params: VariableTemplateParams = variable_params_dialog.exec_and_get_params()

            if params is not None:
                if clb.is_dc_signal[self.current_template.signal_type]:
                    self.current_template.points = [Point(a, 0) for a, f in self.current_template.points]

                self.config_ready.emit(self.current_template, params)
                self.reject()

    def filter_templates(self, a_text):
        for row in range(self.ui.templates_list.count()):
            item = self.ui.templates_list.item(row)
            item.setHidden(a_text.lower() not in item.text().lower())

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        self.settings.save_header_state(self.__class__.__name__, self.points_table.get_header_state())
        a_event.accept()


class PointsDataTable:
    class PointCols(IntEnum):
        AMPLITUDE = 0
        FREQUENCY = 1

    def __init__(self, a_signal_type: clb.SignalType, a_table_widget: QtWidgets.QTableWidget):
        self.table: QtWidgets.QTableWidget = a_table_widget
        self.table.setItemDelegate(TableEditDoubleClick(self.table))

        self.signal_type = a_signal_type
        self.units = clb.signal_type_to_units[self.signal_type]
        self.value_to_user = utils.value_to_user_with_units(self.units)

        # noinspection PyUnresolvedReferences
        self.table.itemChanged.connect(self.set_value_to_user)
        # Нужен, чтобы лишний раз не писать в БД точек, если они не менялись при изменении шаблона
        self.points_were_edited = False

    def restore_header_state(self, a_state: QtCore.QByteArray):
        return self.table.horizontalHeader().restoreState(a_state)

    def get_header_state(self):
        return self.table.horizontalHeader().saveState()

    def append_point(self, _: bool, a_amplitude: float = 0, a_frequency: float = 0):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, self.PointCols.AMPLITUDE, QtWidgets.QTableWidgetItem(str(a_amplitude)))
        self.table.setItem(row, self.PointCols.FREQUENCY, QtWidgets.QTableWidgetItem(str(a_frequency)))
        self.points_were_edited = True

    def delete_selected_points(self):
        rows = self.table.selectionModel().selectedRows()
        if rows:
            for idx_model in reversed(rows):
                self.table.removeRow(idx_model.row())
            self.points_were_edited = True

    def get_points(self):
        points = []
        try:
            for row in range(self.table.rowCount()):
                points.append(Point(amplitude=utils.parse_input(self.table.item(row, self.PointCols.AMPLITUDE).text()),
                                    frequency=float(self.table.item(row, self.PointCols.FREQUENCY).text())))
        except ValueError as err:
            points.clear()
            print("get_points ValueError! ", err)
        return points

    def reset(self, a_points: list):
        qt_utils.qtablewidget_clear(self.table)
        for point in a_points:
            qt_utils.qtablewidget_append_row(self.table, point)

    def set_value_to_user(self, a_item: QtWidgets.QTableWidgetItem):
        self.table.blockSignals(True)
        try:
            if a_item.column() == self.PointCols.AMPLITUDE:
                value_f = utils.parse_input(a_item.text())
                value_f = clb.bound_amplitude(value_f, self.signal_type)
                value_str = self.value_to_user(value_f)
            else:
                value_f = float(a_item.text())
                value_f = clb.bound_frequency(value_f, self.signal_type)
                value_str = utils.float_to_string(value_f)

            a_item.setText(value_str)
            a_item.setData(QtCore.Qt.UserRole, value_str)
            self.points_were_edited = True

        except ValueError:
            a_item.setText(a_item.data(QtCore.Qt.UserRole))
        self.table.blockSignals(False)

    def clear_points_edited_state(self):
        self.points_were_edited = False

    def were_points_edited(self):
        return self.points_were_edited

    def set_signal_type(self, a_signal_type: clb.SignalType):
        if self.signal_type != a_signal_type:
            self.signal_type = a_signal_type

            self.units = clb.signal_type_to_units[self.signal_type]
            self.value_to_user = utils.value_to_user_with_units(self.units)

            for row in range(self.table.rowCount()):
                item = self.table.item(row, self.PointCols.AMPLITUDE)
                value_f: float = utils.parse_input(item.text())
                value_f = clb.bound_amplitude(value_f, self.signal_type)
                item.setText(self.value_to_user(value_f))
