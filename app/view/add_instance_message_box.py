from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, TitleLabel, BodyLabel, LineEdit, ComboBox, TransparentPushButton, FluentIcon


class AddInstanceMessageBox(MessageBoxBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.titleLabel = TitleLabel(self.tr('Add Instance'), self)
        self.addressLabel = BodyLabel(self.tr('Address'), self)
        self.addressInput = LineEdit(self)
        self.simulatorLabel = BodyLabel(self.tr('Simulator'), self)
        self.simulatorInput = ComboBox(self)
        self.moreButton = TransparentPushButton(FluentIcon.CARE_DOWN_SOLID, self.tr('More'), self)

        self.addressLayout = QHBoxLayout()
        self.simulatorLayout = QHBoxLayout()
        self.moreLayout = QHBoxLayout()

        self.addressInput.setClearButtonEnabled(True)
        simulators = [self.tr('MuMu Simulator')]
        self.simulatorInput.addItems(simulators)
        self.moreButton.setLayoutDirection(Qt.RightToLeft)

        self.addressLayout.addWidget(self.addressLabel)
        self.addressLayout.addWidget(self.addressInput)
        self.simulatorLayout.addWidget(self.simulatorLabel)
        self.simulatorLayout.addWidget(self.simulatorInput)
        self.moreLayout.addStretch(1)
        self.moreLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

        self.viewLayout.addWidget(self.titleLabel, 1)
        self.viewLayout.addLayout(self.addressLayout, 1)
        self.viewLayout.addLayout(self.simulatorLayout, 1)
        self.viewLayout.addLayout(self.moreLayout, 0)

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.addressInput.textChanged.connect(self._validateAddress)

    def _validateAddress(self, text):
        if text:
            self.yesButton.setEnabled(True)

