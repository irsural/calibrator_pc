from typing import List

from PyQt5 import QtCore, QtWidgets

from ui.py.template_scales_tabwidget import Ui_Form as ScalesWidgetForm
from custom_widgets.EditListDialog import EditedListOnlyNumbers
from scale_limits_dialog import ScaleLimitsDialog
from db_templates import TemplatesDB
import constants as cfg
import utils


class ScalesWidget(QtWidgets.QWidget):
    tab_added = QtCore.pyqtSignal()
    tab_removed = QtCore.pyqtSignal(int)

    def __init__(self, a_templates_db: TemplatesDB, a_parent=None):
        super().__init__(a_parent)

        self.ui = ScalesWidgetForm()
        self.ui.setupUi(self)
        self.parent = a_parent

        self.scales_id: dict = {}

        self.template_id = 0
        self.templates_db = a_templates_db

        self.set_up_tab_widget()

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
        assert self.template_id != 0, "self.template_id must not be 0!"
        self.add_new_tab(self.template_id)

    def reset(self, a_template_id: int, a_scales: List[cfg.Scale]):
        for tab_idx in range(self.ui.tabWidget.count() - 1):
            self.ui.tabWidget.removeTab(0)

        self.template_id = a_template_id
        self.scales_id.clear()
        for scale in a_scales:
            self.add_new_tab(self.template_id, scale)
        self.ui.tabWidget.setCurrentIndex(0)

    def add_new_tab(self, a_template_id: int, a_scale: cfg.Scale = None):
        try:
            new_tab_index = self.ui.tabWidget.count() - 1

            if a_scale is None:
                a_scale = self.templates_db.new_scale(a_template_id, a_scale)
                a_scale.number = new_tab_index

            config_scale_button = QtWidgets.QPushButton("Пределы", self)
            config_scale_button.clicked.connect(self.edit_scale_limits)
            scale_list = EditedListOnlyNumbers(parent=self, a_init_items=(p for p in a_scale.points),
                                               a_optional_widget=config_scale_button)

            self.ui.tabWidget.insertTab(new_tab_index, scale_list, str(self.ui.tabWidget.count()))
            self.ui.tabWidget.setCurrentIndex(new_tab_index)

            self.scales_id[new_tab_index + 1] = a_scale.id

        except Exception as err:
            utils.exception_handler(err)

    def remove_tab(self, a_idx: int):
        try:
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
                    self.templates_db.delete_scale(self.scales_id[a_idx + 1])

                    # Последнюю вкладку с плюсиком не переименовываем
                    for tab_idx in range(self.ui.tabWidget.count() - 1):
                        old_scale_number = int(self.ui.tabWidget.tabText(tab_idx))
                        actual_scale_number = tab_idx + 1
                        actual_tab_name = str(actual_scale_number)
                        if self.ui.tabWidget.tabText(tab_idx) != actual_tab_name:
                            scale_id = self.scales_id[old_scale_number]
                            del self.scales_id[old_scale_number]
                            self.scales_id[actual_scale_number] = scale_id

                            self.ui.tabWidget.setTabText(tab_idx, actual_tab_name)
        except Exception as err:
            utils.exception_handler(err)

    def edit_scale_limits(self):
        try:
            current_scale_number = self.ui.tabWidget.currentIndex() + 1
            scale_id = self.scales_id[current_scale_number]
            limits: List[cfg.Scale.Limit] = self.templates_db.get_limits(scale_id)

            scale_limits_dialog = ScaleLimitsDialog(limits, self)

            new_limits, deleted_ids = scale_limits_dialog.exec_and_get_limits()
            if new_limits is not None:
                # Вносим изменения в базу, только если пользователь подтвердил ввод
                self.templates_db.delete_limits(deleted_ids)
                print(deleted_ids)
                for limit in new_limits:
                    if limit.id != 0:
                        print("update", limit.id)
                        self.templates_db.update_limit(limit)
                    else:
                        print("insert", limit.id)
                        self.templates_db.new_limit(scale_id, limit)
        except Exception as err:
            utils.exception_handler(err)

    def get_scales(self) -> List[cfg.Scale]:
        scales = [self.get_scale_by_tab_idx(tab_idx) for tab_idx in range(self.ui.tabWidget.count() - 1)]
        return scales

    def get_scale_by_tab_idx(self, a_tab_idx):
        scale_points_list: EditedListOnlyNumbers = self.ui.tabWidget.widget(a_tab_idx)
        scale_number = a_tab_idx + 1
        # Пределы обновляются в базе сразу после изменения, их передавать не нужно
        return cfg.Scale(a_id=self.scales_id[scale_number], a_number=scale_number,
                         a_scale_points=scale_points_list.get_list())
