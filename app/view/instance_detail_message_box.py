from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, BodyLabel, LineEdit, ComboBox

from app.common.maa.emulators import Emulator
from app.common.maa.instance.maa_instance import MaaInstance
from app.common.maa.instance.maa_instance_manager import maaInstanceManager
from app.common.signal_bus import signalBus


class InstanceDetailMessageBox(MessageBoxBase):
    def __init__(self, parent, instance: MaaInstance):
        super().__init__(parent)
        self.instance = instance

        self.titleLabel = TitleLabel(self.tr('Instance Settings'), self)
        self.nameLabel = BodyLabel(self.tr('Name'), self)
        self.nameInput = LineEdit(self)
        self.addressLabel = BodyLabel(self.tr('Address'), self)
        self.addressInput = LineEdit(self)
        self.emulatorLabel = BodyLabel(self.tr('Emulator'), self)
        self.emulatorInput = ComboBox(self)

        self.nameLayout = QHBoxLayout()
        self.addressLayout = QHBoxLayout()
        self.simulatorLayout = QHBoxLayout()

        self.nameInput.setText(self.instance.name)
        self.addressInput.setText(self.instance.connection.address)

        self.addressInput.setClearButtonEnabled(True)
        self.addressInput.setPlaceholderText('127.0.0.1:16384')
        for emulator in Emulator:
            value = emulator.value
            self.emulatorInput.addItem(self.tr(value), Emulator.getIcon(value), value)

        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameInput)
        self.addressLayout.addWidget(self.addressLabel)
        self.addressLayout.addWidget(self.addressInput)
        self.simulatorLayout.addWidget(self.emulatorLabel)
        self.simulatorLayout.addWidget(self.emulatorInput)

        self.viewLayout.addWidget(self.titleLabel, 1)
        self.viewLayout.addLayout(self.nameLayout, 1)
        self.viewLayout.addLayout(self.addressLayout, 1)
        self.viewLayout.addLayout(self.simulatorLayout, 1)

        self.widget.setMinimumWidth(350)
        self.addressInput.textChanged.connect(self._validateAddress)
        self.yesButton.clicked.connect(self.save)

    def _validateAddress(self, text):
        if text:
            self.yesButton.setEnabled(True)

    def save(self):
        self.instance.name = self.nameInput.text()
        self.instance.connection.address = self.addressInput.text()
        self.instance.connection.emulator = self.emulatorInput.currentData()
        maaInstanceManager.refreshInstance(self.instance)
        signalBus.instanceChanged.emit(str(self.instance.uid))
