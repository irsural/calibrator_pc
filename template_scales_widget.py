from typing import List
import sys

from PyQt5 import QtCore, QtWidgets

from ui.py.template_scales_tabwidget import Ui_Form as ScalesWidgetForm
from custom_widgets.EditListDialog import EditedListOnlyNumbers
from scale_limits_dialog import ScaleLimitsDialog
import constants as cfg
import utils


class ScalesWidget(QtWidgets.QWidget):
    tab_added = QtCore.pyqtSignal()
    tab_removed = QtCore.pyqtSignal(int)

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.ui = ScalesWidgetForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        # self.scale_limits: dict = {}

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

    def append_scale(self, a_scale: cfg.Scale):
        self.add_new_tab(a_scale.points)

    def add_new_tab(self, a_init_items=()):
        try:
            config_scale_button = QtWidgets.QPushButton("Пределы", self)
            config_scale_button.clicked.connect(self.edit_scale_limits)
            scale_list = EditedListOnlyNumbers(parent=self, a_init_items=a_init_items,
                                               a_optional_widget=config_scale_button)

            # self.scale_limits[scale_list] = [cfg.Scale.Limit()]

            new_tab_index = self.ui.tabWidget.count() - 1
            self.ui.tabWidget.insertTab(new_tab_index, scale_list, str(self.ui.tabWidget.count()))
            self.ui.tabWidget.setCurrentIndex(new_tab_index)
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

    def edit_scale_limits(self):
        current_widget = self.ui.tabWidget.currentWidget()
        limits: List[cfg.Scale.Limit] = self.scale_limits[current_widget]

        scale_limits_dialog = ScaleLimitsDialog(limits)
        new_limits = scale_limits_dialog.exec_and_get_limits()
        if new_limits is not None:
            self.scale_limits[current_widget] = new_limits

    def get_scales(self) -> List[cfg.Scale]:
        scales = [self.get_scale_by_tab_idx(tab_idx) for tab_idx in range(self.ui.tabWidget.count() - 1)]
        return scales

    def get_scale_by_tab_idx(self, a_tab_idx):
        scale_points_list: EditedListOnlyNumbers = self.ui.tabWidget.widget(a_tab_idx)
        return cfg.Scale(a_scale_points=scale_points_list.get_list(), a_limits=self.scale_limits[scale_points_list])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ScalesWidget()
    w.show()
    sys.exit(app.exec())
