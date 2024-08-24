from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import FlowLayout, LargeTitleLabel


class CardFlowView(QWidget):
    def __init__(self, title: str = None, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        if title:
            self.vBoxLayout.addWidget(LargeTitleLabel(title, self))
        self.flowLayout = FlowLayout(needAni=True)
        self.vBoxLayout.addLayout(self.flowLayout)
        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.flowLayout.setContentsMargins(0, 8, 0, 8)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

    def addCard(self, card: QWidget):
        self.flowLayout.addWidget(card)
