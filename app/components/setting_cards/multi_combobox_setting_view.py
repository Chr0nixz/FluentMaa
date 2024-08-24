import json

from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard

from app.components.multiselection_combobox import MultiSelectionComboBox


class MultiComboBoxSettingCard(SettingCard):
    def __init__(self, icon, title, selections: list,
                 content=None,  text: str = 'Select',
                 config=None, name=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.comboBox = MultiSelectionComboBox(self.tr(text), self)
        self.comboBox.setFixedHeight(30)
        if config and name:
            try:
                default = getattr(config, name)
                if default:
                    self.selected = default
                    print(type(self.selected))
            except AttributeError:
                pass
        for i in selections:
            self.comboBox.addItem(i)
        for i in self.selected:
            self.comboBox.check(i)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.comboBox, 1)
        self.hBoxLayout.setContentsMargins(12, 0, 12, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comboBox.valueChanged.connect(self.changeValue)
        self.config = config
        self.name = name
        #self.setFixedHeight(60)

    def changeValue(self):
        if self.config and self.name:
            setattr(self.config, self.name, self.comboBox.getValue())
