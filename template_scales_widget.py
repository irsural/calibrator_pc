import ui_to_py
ui_to_py.convert_ui("./ui", "./ui/py")
ui_to_py.convert_resources("./resources", "./resources/py")

from enum import IntEnum
import sys

from PyQt5 import QtCore, QtWidgets, QtGui


from ui.py.template_scales_tabwidget import Ui_Form as ScalesWidgetForm
from custom_widgets.EditListDialog import EditedListOnlyNumbers
import calibrator_constants as clb
import qt_utils
import utils


class ScalesWidget(QtWidgets.QWidget):
    tab_added = QtCore.pyqtSignal()
    tab_removed = QtCore.pyqtSignal(int)

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = ScalesWidgetForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.set_up_tab_widget()
        self.add_new_tab()

    def __del__(self):
        print("scales widget deleted")

    def set_up_tab_widget(self):
        plus_button = QtWidgets.QPushButton("+")
        plus_button.setFlat(True)
        plus_button.setFixedSize(20, 20)
        self.ui.tabWidget.addTab(QtWidgets.QWidget(), "")
        self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.count() - 1, False)
        self.ui.tabWidget.tabBar().setTabButton(self.ui.tabWidget.count() - 1, QtWidgets.QTabBar.RightSide, plus_button)
        self.ui.tabWidget.tabCloseRequested.connect(self.remove_tab)
        plus_button.clicked.connect(self.plus_button_clicked)

    def plus_button_clicked(self):
        self.add_new_tab()

    def add_new_tab(self, a_init_items=()):
        try:
            config_scale_button = QtWidgets.QPushButton("Пределы шкалы", self)
            config_scale_button.clicked.connect(self.edit_scale_limits)
            scale_list = EditedListOnlyNumbers(parent=self, a_init_items=a_init_items,
                                               a_optional_widget=config_scale_button)

            new_tab_index = self.ui.tabWidget.count() - 1
            self.ui.tabWidget.insertTab(new_tab_index, scale_list, str(self.ui.tabWidget.count()))
            self.ui.tabWidget.setCurrentIndex(new_tab_index)
            self.tab_added.emit()
        except Exception as err:
            utils.exception_handler(err)

    def remove_tab(self, a_idx: int):
        if self.ui.tabWidget.count() > 2:
            res = QtWidgets.QMessageBox.question(self, "Подтвердите действие",
                                                 f"Вы действительно хотите удалить шкалу №{a_idx + 1}?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                 QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.Yes:
                if a_idx == self.ui.tabWidget.count() - 2 and a_idx == self.ui.tabWidget.currentIndex():
                    # Если удаляемая вкладка активна, меняем активную на предыдущую
                    self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 3)
                self.ui.tabWidget.removeTab(a_idx)

                # Последнюю вкладку с плюсиком не переименовываем
                for tab_idx in range(self.ui.tabWidget.count() - 1):
                    actual_tab_name = str(tab_idx + 1)
                    if self.ui.tabWidget.tabText(tab_idx) != actual_tab_name:
                        self.ui.tabWidget.setTabText(tab_idx, actual_tab_name)

                self.tab_removed.emit(a_idx)

    def edit_scale_limits(self):
        print(self.ui.tabWidget.currentIndex())

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ScalesWidget()
    w.show()
    sys.exit(app.exec())


