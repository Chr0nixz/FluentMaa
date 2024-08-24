from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from qfluentwidgets import TransparentDropDownPushButton, FluentIcon, CheckableMenu, MenuIndicatorType, Action


class MultiSelectionComboBox(QWidget):

    valueChanged = Signal()
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.items = {}

        self.button = TransparentDropDownPushButton(self.tr(self.title), self)
        self.menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.CHECK)
        self.button.setMenu(self.menu)

    def addItem(self, item: str):
        action = Action(self.tr(item), checkable=True, triggered=lambda: self.valueChanged.emit())
        self.items[item] = action
        self.menu.addAction(action)

    def getValue(self):
        result = []
        for i in self.items.items():
            if i[1].isChecked():
                result.append(i[0])
        return result

    def check(self, item: str):
        self.items[item].setChecked(True)

