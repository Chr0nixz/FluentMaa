from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, BodyLabel, LineEdit, TransparentPushButton, ComboBox, FluentIcon

from app.common.maa.emulators import Emulator


class InstanceDetailMessageBox(MessageBoxBase):
    def __init__(self, parent, instance_config: dict):
        super().__init__(parent)
        self.config = instance_config

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

        self.nameInput.setText(self.config['name'])
        self.addressInput.setText(self.config['connection']['address'])

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
        self.yesButton.setDisabled(True)
        self.addressInput.textChanged.connect(self._validateAddress)

    def _validateAddress(self, text):
        if text:
            self.yesButton.setEnabled(True)