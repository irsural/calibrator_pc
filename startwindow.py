from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore

from ui.py.startform import Ui_Form as StartForm
from settings_ini_parser import Settings


class StartWindow(QtWidgets.QWidget):
    source_mode_chosen = pyqtSignal()
    no_template_mode_chosen = pyqtSignal()
    template_mode_chosen = pyqtSignal()

    def __init__(self, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = StartForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.settings = a_settings

        self.setWindowTitle("Калибратор N4-25")

        self.ui.source_mode_button.clicked.connect(self.source_mode_chosen)
        self.ui.no_template_mode_button.clicked.connect(self.no_template_mode_chosen)
        self.ui.template_mode_button.clicked.connect(self.template_mode_chosen)

        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.parent.show()
        # По каким то причинам restoreGeometry не восстанавливает размер ЭТОГО окна, если оно скрыто
        self.parent.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))


    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.parent.saveGeometry())
        a_event.accept()



