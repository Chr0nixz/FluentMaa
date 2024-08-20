from PySide6.QtCore import Qt
from qfluentwidgets import SpinBox, SettingCard


class SpinBoxSettingCard(SettingCard):
    def __init__(self, icon, title, content=None, config=None, name=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.spinbox = SpinBox()
        self.spinbox.setRange(0, 99)
        if config and name:
            try:
                default = getattr(config, name)
                if default:
                    self.spinbox.setValue(default)
            except AttributeError:
                pass
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.spinbox, 1)
        self.hBoxLayout.setContentsMargins(12, 0, 12, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinbox.valueChanged.connect(self.changeValue)
        self.config = config
        self.name = name

    def changeValue(self, value):
        if self.config and self.name:
            setattr(self.config, self.name, value)