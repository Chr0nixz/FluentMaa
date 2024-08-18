from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import CardWidget, TransparentPushButton, TransparentToolButton, FluentIcon, isDarkTheme, \
    StrongBodyLabel


class TaskCard(CardWidget):

    def __init__(self, index: int, task: dict, parent=None):
        super().__init__(parent)

        self.indexLabel = StrongBodyLabel(str(index + 1), self)
        self.taskButton = TransparentPushButton(task['type'], self)
        self.removeButton = TransparentToolButton(FluentIcon.CLOSE.colored(QColor(0, 0, 0, 15), QColor(255, 255, 255, 21)), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(8, 0, 0, 0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.addWidget(self.indexLabel)
        self.hBoxLayout.addWidget(self.taskButton)
        self.hBoxLayout.addWidget(self.removeButton)

        self.setLayout(self.hBoxLayout)

    def remove(self):
        self.parent().removeWidget(self)
        self.setParent(None)
        self.deleteLater()
