from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal


from ui.py.source_mode_form import Ui_source_mode_dialog as SourceModeForm
from irspy.qt.custom_widgets.source_mode_widget import SourceModeWidget
from irspy.qt.qt_settings_ini_parser import QtSettings
import irspy.clb.calibrator_constants as clb
import irspy.clb.clb_dll as clb_dll


class SourceModeDialog(QtWidgets.QDialog):
    close_confirmed = pyqtSignal()

    def __init__(self, a_settings: QtSettings, a_calibrator: clb_dll.ClbDrv, a_parent=None):
        super().__init__(a_parent)

        self.ui = SourceModeForm()
        self.ui.setupUi(self)

        self.settings = a_settings
        self.calibrator = a_calibrator
        self.source_mode_widget = SourceModeWidget(self.settings, self.calibrator, self)
        self.layout().addWidget(self.source_mode_widget)

    def update_clb_list(self, a_clb_list: list):
        self.source_mode_widget.update_clb_list(a_clb_list)

    def update_clb_status(self, a_status: clb.State):
        self.source_mode_widget.update_clb_status(a_status)

    def signal_enable_changed(self, a_enable):
        self.source_mode_widget.signal_enable_changed(a_enable)

    def __del__(self):
        print("source mode deleted")

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.calibrator.signal_enable = False
