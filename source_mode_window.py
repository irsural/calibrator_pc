from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from ui.py.source_mode_form import Ui_Form as SourceModeForm
import clb_dll

import calibrator_constants as clb
import utils


class SourceModeWindow(QWidget):
    window_is_closed = pyqtSignal()

    def __init__(self, a_calibrator: clb_dll.ClbDrv):
        super().__init__()

        self.ui = SourceModeForm()
        self.ui.setupUi(self)

        self.calibrator = a_calibrator

        self.connect_signals()

        self.clb_params = clb.ClbParams()
        self.int_to_signal_type = {
            clb.SignalType.ACI: self.ui.aci_radio,
            clb.SignalType.ACV: self.ui.acv_radio,
            clb.SignalType.DCI: self.ui.dci_radio,
            clb.SignalType.DCV: self.ui.dcv_radio,
        }
        self.int_to_mode = {
            clb.Mode.SOURCE: self.ui.source_mode_radio,
            clb.Mode.FIXED_RANGE: self.ui.fixed_mode_radio,
            clb.Mode.DETUNING: self.ui.detuning_radio,
        }

        self.clb_check_timer = QTimer()
        self.clb_check_timer.timeout.connect(self.sync_clb_parameters)
        self.clb_check_timer.start(10)

        self.block_signals = False

    def connect_signals(self):
        self.ui.clb_list_combobox.currentTextChanged.connect(self.connect_to_clb)
        self.ui.amplitude_edit.textChanged.connect(self.amplitude_edit_text_changed)
        self.ui.frequency_spinbox.valueChanged.connect(self.set_frequency)

        self.ui.aci_radio.toggled.connect(self.aci_radio_checked)
        self.ui.acv_radio.toggled.connect(self.acv_radio_checked)
        self.ui.dci_radio.toggled.connect(self.dci_radio_checked)
        self.ui.dcv_radio.toggled.connect(self.dcv_radio_checked)

        self.ui.polarity_button.clicked.connect(self.polarity_button_clicked)

        self.ui.source_mode_radio.toggled.connect(self.source_radio_checked)
        self.ui.fixed_mode_radio.toggled.connect(self.fixed_radio_checked)
        self.ui.detuning_radio.toggled.connect(self.detuning_radio_checked)

        self.ui.enable_button.clicked.connect(self.signal_enable)

    @pyqtSlot(list)
    def update_clb_list(self, a_clb_list: list):
        self.ui.clb_list_combobox.clear()
        for clb_name in a_clb_list:
            self.ui.clb_list_combobox.addItem(clb_name)

    @pyqtSlot(str)
    def update_clb_status(self, a_status: str):
        self.ui.usb_state_label.setText(a_status)

    def connect_to_clb(self, a_clb_name):
        self.calibrator.connect(a_clb_name)

    def sync_clb_parameters(self):
        self.block_signals = True

        if self.calibrator.amplitude_changed():
            self.ui.amplitude_edit.setText(f"{self.calibrator.amplitude:.9f}")

        if self.calibrator.frequency_changed():
            self.ui.frequency_spinbox.setValue(self.calibrator.frequency)

        if self.calibrator.signal_type_changed():
            self.int_to_signal_type[self.calibrator.signal_type].setChecked(True)

        if self.calibrator.polarity_changed():
            self.ui.polarity_button.setText(clb.int_to_polarity[self.calibrator.polarity])
            if self.calibrator.polarity == clb.Polatiry.POS:
                self.ui.polarity_button.setChecked(False)
            else:
                self.ui.polarity_button.setChecked(True)

        if self.calibrator.signal_enable_changed():
            if self.calibrator.signal_enable:
                self.ui.enable_button.setChecked(True)
                self.ui.enable_button.setText("Disable")
            else:
                self.ui.enable_button.setChecked(False)
                self.ui.enable_button.setText("Enable")

        if self.calibrator.mode_changed():
            self.int_to_mode[self.calibrator.mode].setChecked(True)

        self.block_signals = False

    def amplitude_edit_text_changed(self):
        if not self.block_signals:
            utils.update_edit_color(self.calibrator.amplitude, self.ui.amplitude_edit)

    def set_frequency(self):
        if not self.block_signals:
            self.calibrator.frequency = self.ui.frequency_spinbox.value()

    def aci_radio_checked(self):
        if not self.block_signals:
            self.calibrator.signal_type = clb.SignalType.ACI

    def acv_radio_checked(self):
        if not self.block_signals:
            self.calibrator.signal_type = clb.SignalType.ACV

    def dci_radio_checked(self):
        if not self.block_signals:
            self.calibrator.signal_type = clb.SignalType.DCI

    def dcv_radio_checked(self):
        if not self.block_signals:
            self.calibrator.signal_type = clb.SignalType.DCV

    def polarity_button_clicked(self, a_checked):
        if not self.block_signals:
            if a_checked:
                self.calibrator.polarity = clb.Polatiry.NEG
                self.ui.polarity_button.setText(clb.int_to_polarity[clb.Polatiry.NEG])
            else:
                self.calibrator.polarity = clb.Polatiry.POS
                self.ui.polarity_button.setText(clb.int_to_polarity[clb.Polatiry.POS])

    def signal_enable(self, a_enable):
        if not self.block_signals:
            self.calibrator.signal_enable = int(a_enable)

    def source_radio_checked(self):
        if not self.block_signals:
            self.calibrator.mode = clb.Mode.SOURCE

    def fixed_radio_checked(self):
        if not self.block_signals:
            self.calibrator.mode = clb.Mode.FIXED_RANGE

    def detuning_radio_checked(self):
        if not self.block_signals:
            self.calibrator.mode = clb.Mode.DETUNING

    def closeEvent(self, event):
        print("here1")
        self.hide()
        self.window_is_closed.emit()
        print("here3")
