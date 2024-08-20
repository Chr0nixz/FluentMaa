from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard, SwitchButton


class SwitchButtonSettingCard(SettingCard):
    def __init__(self, icon, title, content=None, config=None, name=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.switchButton = SwitchButton()
        if config and name:
            try:
                default = getattr(config, name)
                if default:
                    self.switchButton.setEnabled(default)
            except AttributeError:
                pass
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.switchButton, 1)
        self.hBoxLayout.setContentsMargins(12, 0, 12, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.switchButton.checkedChanged.connect(self.changeValue)
        self.config = config
        self.name = name

    def changeValue(self, value):
        if self.config and self.name:
            setattr(self.config, self.name, value)