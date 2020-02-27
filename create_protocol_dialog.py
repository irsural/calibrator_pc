from sqlite3 import Connection

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.py.create_protocol_form import Ui_Dialog as CreateProtocolForm
from db_measures import MeasureParams, MeasureTables, MeasuresDB
from settings_ini_parser import Settings
from marks_widget import MarksWidget


class CreateProtocolDialog(QtWidgets.QDialog):
    def __init__(self, a_settings: Settings, a_measure_id: int, a_db_connection: Connection,
                 a_db_tables: MeasureTables, a_parent=None):
        super().__init__(a_parent)

        self.ui = CreateProtocolForm()
        self.ui.setupUi(self)

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        assert a_measure_id != 0, "Measure id must not be zero!"

        self.measure_db = MeasuresDB(a_db_connection, a_db_tables)
        self.measure_config, points = self.measure_db.get(a_measure_id)

        self.marks_widget = MarksWidget(self.settings, a_db_connection, a_db_tables,
                                        a_measure_id=self.measure_config.id, a_parent=self)
        self.ui.marks_widget_layout.addWidget(self.marks_widget)

        self.set_up_params_to_ui(points)

        self.ui.accept_button.clicked.connect(self.save_pressed)
        self.ui.reject_button.clicked.connect(self.reject)

    def set_up_params_to_ui(self, a_points):
        self.ui.user_name_edit.setText(self.measure_config.user)
        self.ui.device_name_edit.setText(self.measure_config.device_name)
        self.ui.serial_number_edit.setText(self.measure_config.serial_num)
        self.ui.owner_edit.setText(self.measure_config.owner)
        self.ui.device_creator_edit.setText(self.measure_config.device_creator)
        self.ui.date_edit.setDate(QtCore.QDate.fromString(self.measure_config.date, "dd.MM.yyyy"))

        self.ui.organisation_edit.setText(self.measure_config.organisation)
        self.ui.system_combobox.setCurrentIndex(self.measure_config.device_system)
        self.ui.comment_edit.setText(self.measure_config.comment)

        self.ui.signal_type_combobox.setCurrentIndex(self.measure_config.signal_type)
        self.ui.class_spinbox.setValue(self.measure_config.device_class)
        self.ui.etalon_edit.setText(self.measure_config.etalon_device)

        # Восстановить точки

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
        self.measure_config.etalon_device = self.ui.etalon_edit.text()
        self.measure_config.device_class = self.ui.class_spinbox.value()

        # Сохранить точки
        # Сохранить в БД

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        # Вызывается вручную, чтобы marks_widget сохранил состояние своего хэдера
        self.marks_widget.close()
        a_event.accept()
