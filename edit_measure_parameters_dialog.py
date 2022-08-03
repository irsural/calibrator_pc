from sqlite3 import Connection

from PyQt5 import QtCore, QtGui, QtWidgets

from ui.py.edit_measure_parameters_form import Ui_edit_measure_params_dialog as EditMeasureParamsForm
from marks_widget import MarksWidget
from db_measures import Measure
from irspy.qt.qt_settings_ini_parser import QtSettings


class EditMeasureParamsDialog(QtWidgets.QDialog):
    def __init__(self, a_settings: QtSettings, a_measure_config: Measure, a_db_connection: Connection,
                 a_parent=None):
        super().__init__(a_parent)

        self.ui = EditMeasureParamsForm()
        self.ui.setupUi(self)
        self.ui.default_button.setHidden(True)

        self.settings = a_settings
        self.settings.restore_qwidget_state(self)

        self.measure_config = a_measure_config

        assert a_measure_config.id != 0, "Measure id must not be zero!"
        self.marks_widget = MarksWidget(self.__class__.__name__, self.settings, a_db_connection,
                                        a_measure_id=self.measure_config.id, a_parent=None)
        self.ui.marks_widget_layout.addWidget(self.marks_widget)

        self.set_up_params_to_ui()

        self.ui.accept_button.clicked.connect(self.save_pressed)
        self.ui.reject_button.clicked.connect(self.cancel_pressed)

    def __del__(self):
        print("edit parameters deleted")

    def set_up_params_to_ui(self):
        self.ui.user_name_edit.setText(self.measure_config.user)
        self.ui.device_name_edit.setText(self.measure_config.device_name)
        self.ui.serial_number_edit.setText(self.measure_config.serial_num)
        self.ui.owner_edit.setText(self.measure_config.owner)
        self.ui.device_creator_edit.setText(self.measure_config.device_creator)
        self.ui.date_edit.setDate(QtCore.QDate.fromString(self.measure_config.date, "dd.MM.yyyy"))

        self.ui.system_combobox.setCurrentIndex(self.measure_config.device_system)
        self.ui.comment_edit.setText(self.measure_config.comment)

    def save_pressed(self):
        self.save()
        if self.marks_widget.save():
            self.save_geometry()
            self.accept()

    def cancel_pressed(self):
        self.save_geometry()
        self.reject()

    def save(self):
        self.measure_config.user = self.ui.user_name_edit.text()
        self.measure_config.device_name = self.ui.device_name_edit.text()
        self.measure_config.serial_num = self.ui.serial_number_edit.text()
        self.measure_config.owner = self.ui.owner_edit.text()
        self.measure_config.device_creator = self.ui.device_creator_edit.text()
        self.measure_config.date = self.ui.date_edit.text()
        self.measure_config.device_system = self.ui.system_combobox.currentIndex()
        self.measure_config.comment = self.ui.comment_edit.text()

    def save_geometry(self):
        self.settings.save_qwidget_state(self)
        # Вызывается вручную, чтобы marks_widget сохранил состояние своего хэдера
        self.marks_widget.close()

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.save_geometry()
        a_event.accept()
