from re import compile as re_compile
from sqlite3 import Connection
from typing import List, Tuple, Union, Iterable
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.py.create_protocol_form import Ui_Dialog as CreateProtocolForm
from measure_cases_widget import MeasureCases
from db_measures import MeasuresDB
from settings_ini_parser import Settings
from marks_widget import MarksWidget
import calibrator_constants as clb
import constants as cfg
import odf_output
import utils


class CreateProtocolDialog(QtWidgets.QDialog):
    GET_MARK_RE = re_compile(r"%.*__")

    def __init__(self, a_settings: Settings, a_measure_id: int, a_db_connection: Connection, a_parent=None):
        super().__init__(a_parent)

        self.ui = CreateProtocolForm()
        self.ui.setupUi(self)
        self.ui.default_button.setHidden(True)

        assert a_measure_id != 0, "Measure id must not be zero!"

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        self.measure_db = MeasuresDB(a_db_connection)
        self.measure_config = self.measure_db.get(a_measure_id)

        self.marks_widget = MarksWidget(self.settings, a_db_connection, a_measure_id=self.measure_config.id)
        self.ui.marks_widget_layout.addWidget(self.marks_widget)

        self.default_marks_widgets = self.get_default_marks_widgets()
        self.set_up_params_to_ui()

        self.ui.points_table.horizontalHeader().restoreState(self.settings.get_last_header_state(
            self.__class__.__name__))
        self.ui.points_table.horizontalHeader().setSectionsMovable(True)

        self.measure_manager = MeasureCases(self.ui.points_table, self.measure_config.cases, a_allow_editing=False)
        self.ui.cases_bar_layout.addWidget(self.measure_manager.cases_bar)

        self.connect_signals()
        self.ui.marks_and_points_tabwidget.setCurrentIndex(0)

    def connect_signals(self):
        for widgets in self.default_marks_widgets:
            widgets[0].customContextMenuRequested.connect(self.show_label_custom_menu)

        self.ui.choose_protocol_template_button.clicked.connect(self.choose_template_pattern_file)
        self.ui.choose_save_folder_button.clicked.connect(self.choose_save_protocol_folder)

        self.ui.accept_button.clicked.connect(self.save_pressed)
        self.ui.reject_button.clicked.connect(self.reject)

    def get_default_marks_widgets(self):
        default_marks_widgets: List[Tuple[QtWidgets.QLabel, QtWidgets.QWidget]] = [
            (self.ui.date_label, self.ui.date_edit),
            (self.ui.name_label, self.ui.device_name_edit),
            (self.ui.device_creator_label, self.ui.device_creator_edit),
            (self.ui.system_label, self.ui.system_combobox),
            (self.ui.owner_label, self.ui.owner_edit),
            (self.ui.user_label, self.ui.user_name_edit),
            (self.ui.serial_number_label, self.ui.serial_number_edit),
            (self.ui.comment_label, self.ui.comment_edit)
        ]
        return default_marks_widgets

    def show_label_custom_menu(self, a_position: QtCore.QPoint):
        label = self.sender()
        assert isinstance(label, QtWidgets.QLabel), "show_label_custom_menu must be connected to QLabel!"
        menu = QtWidgets.QMenu(label)
        copy_mark_act = menu.addAction("Копировать метку")
        copy_mark_act.triggered.connect(self.copy_label_mark)
        menu.popup(label.mapToGlobal(a_position))

    # noinspection DuplicatedCode
    def set_up_params_to_ui(self):
        self.ui.date_edit.setDate(QtCore.QDate.fromString(self.measure_config.date, "dd.MM.yyyy"))
        self.ui.device_name_edit.setText(self.measure_config.device_name)
        self.ui.device_creator_edit.setText(self.measure_config.device_creator)
        self.ui.owner_edit.setText(self.measure_config.owner)
        self.ui.user_name_edit.setText(self.measure_config.user)
        self.ui.serial_number_edit.setText(self.measure_config.serial_num)

        self.ui.system_combobox.setCurrentIndex(self.measure_config.device_system)
        self.ui.comment_edit.setText(self.measure_config.comment)

        self.ui.template_protocol_edit.setText(self.settings.template_filepath)
        self.ui.save_folder_edit.setText(self.settings.save_folder)

    def copy_label_mark(self):
        # noinspection PyTypeChecker
        label: QtWidgets.QLabel = self.sender().parent().parent()
        assert isinstance(label, QtWidgets.QLabel), "This slot must be called by Qmenu of QLabel!!"

        mark_text = self.extract_mark_from_label(label)
        QtWidgets.QApplication.clipboard().setText(mark_text)

    def extract_mark_from_label(self, label):
        mark_match = self.GET_MARK_RE.search(label.text())
        assert mark_match is not None, "Label must contain mark in format %*__ !!"
        mark_text = mark_match.group(0)
        return mark_text

    # noinspection PyUnresolvedReferences
    def extract_value_from_widget(self, a_widget: QtWidgets.QWidget):
        if isinstance(a_widget, QtWidgets.QLineEdit):
            return a_widget.text()
        elif a_widget == self.ui.date_edit:
            return a_widget.text()
        elif a_widget == self.ui.system_combobox:
            return cfg.enum_to_device_system[a_widget.currentIndex()]
        else:
            assert True, "Unexpected widget"

    def choose_template_pattern_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл, содержащий шаблон протокола",
                                                     self.ui.template_protocol_edit.text(),
                                                     "Текстовый документ ODT (*.odt)")
        filepath = file[0]
        if filepath:
            self.ui.template_protocol_edit.setText(filepath)

    def choose_save_protocol_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите каталог", self.ui.save_folder_edit.text(),
                                                            QtWidgets.QFileDialog.ShowDirsOnly |
                                                            QtWidgets.QFileDialog.DontResolveSymlinks)
        if folder:
            self.ui.save_folder_edit.setText(folder)

    def save_pressed(self):
        try:
            self.save()
            if self.marks_widget.save():
                if self.generate_protocol():
                    self.close()
            else:
                self.ui.marks_and_points_tabwidget.setCurrentIndex(0)
        except Exception as err:
            utils.exception_handler(err)

    # noinspection DuplicatedCode
    def save(self):
        self.measure_config.date = self.ui.date_edit.text()
        self.measure_config.device_name = self.ui.device_name_edit.text()
        self.measure_config.device_creator = self.ui.device_creator_edit.text()
        self.measure_config.device_system = self.ui.system_combobox.currentIndex()

        self.measure_config.owner = self.ui.owner_edit.text()
        self.measure_config.user = self.ui.user_name_edit.text()
        self.measure_config.serial_num = self.ui.serial_number_edit.text()
        self.measure_config.comment = self.ui.comment_edit.text()

        self.measure_db.update_measure(self.measure_config)

        self.settings.template_filepath = self.ui.template_protocol_edit.text()
        self.settings.save_folder = self.ui.save_folder_edit.text()

    def get_src_dst_path(self) -> Union[Tuple[str, str], None]:
        src_file = self.ui.template_protocol_edit.text()
        dst_folder = self.ui.save_folder_edit.text()
        if os.path.exists(src_file) and os.path.isfile(src_file):
            if os.path.exists(dst_folder) and os.path.isdir(dst_folder):
                dst_file = self.generate_filename(dst_folder)
                if os.path.exists(dst_file):
                    res = QtWidgets.QMessageBox.question(self, "Создание протокола",
                                                         "Файл для текущего измерения уже существует.\n"
                                                         "Хотите заменить его?",
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                         QtWidgets.QMessageBox.No)
                    if res == QtWidgets.QMessageBox.Yes:
                        return src_file, dst_file
                    else:
                        return None
                else:
                    return src_file, dst_file
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Путь к каталогу сохранения указан неверно",
                                               QtWidgets.QMessageBox.Ok)
                return None
        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Путь к шаблону протокола указан неверно",
                                           QtWidgets.QMessageBox.Ok)
            return None

    def generate_protocol(self):
        paths = self.get_src_dst_path()
        if paths is not None:
            src_file, dst_file = paths

            marks_map: list = self.marks_widget.get_marks_map()
            for widgets in self.default_marks_widgets:
                marks_map.append((self.extract_mark_from_label(widgets[0]), self.extract_value_from_widget(widgets[1])))

            if odf_output.replace_text_in_odt(src_file, dst_file, marks_map, self.create_tables_to_export()):
                QtWidgets.QMessageBox.information(self, "Успех", "Протокол успешно сгенерирован")
                return True
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "При создании протокола произошла ошибка")
                return False
        else:
            return False

    def generate_filename(self, a_dst_folder: str) -> str:
        dst_folder = a_dst_folder.rstrip("\\").rstrip("/") + os.path.sep
        dst_file = ' '.join([self.measure_config.date,
                             self.measure_config.time.replace(':', '.') + '.',
                             self.measure_config.device_name + ".odt"])
        return os.path.sep.join([os.path.dirname(dst_folder), dst_file])

    def create_tables_to_export(self) -> list:
        exported_tables = []
        for case, table in self.measure_manager.export_tables():
            table_to_draw = odf_output.TableToDraw(case)
            for row in table:
                # Последняя колонка - всегда частота
                table_to_draw.add_point(row[-1], row[:-1])
            exported_tables.append(table_to_draw)
        return exported_tables

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        self.settings.save_header_state(self.__class__.__name__, self.ui.points_table.horizontalHeader().saveState())

        self.measure_manager.close()
        # Вызывается вручную, чтобы marks_widget сохранил состояние своего хэдера
        self.marks_widget.close()
        a_event.accept()

    def __del__(self):
        print("create protocol deleted")
