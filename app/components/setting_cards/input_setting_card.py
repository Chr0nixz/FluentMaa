from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard, LineEdit


class InputSettingCard(SettingCard):
    def __init__(self, icon, title, content=None, config=None, name=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.input = LineEdit(self)
        if config and name:
            try:
                default = getattr(config, name)
                if default:
                    self.input.setText(default)
            except AttributeError:
                pass
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.input, 1)
        self.hBoxLayout.setContentsMargins(12, 0, 12, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input.textChanged.connect(self.changeValue)
        self.config = config
        self.name = name

    def changeValue(self, value):
        if self.config and self.name:
            setattr(self.config, self.name, value)
