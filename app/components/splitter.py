from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QSplitter, QSplitterHandle
from qfluentwidgets import isDarkTheme

from app.common.style_sheet import StyleSheet


class VerticalSplitter(QSplitter):
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)
        StyleSheet.SPLITTER.apply(self)

    def createHandle(self):
        return VerticalSplitterHandle(self)


class VerticalSplitterHandle(QSplitterHandle):
    def __init__(self, parent):
        super().__init__(Qt.Orientation.Vertical, parent)
        self.setFixedHeight(10)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.setProperty('hover', False)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            painter.setBrush(QBrush(QColor("#a1a1a1")))
        else:
            painter.setBrush(QBrush(QColor("#818181")))
        painter.setPen(Qt.PenStyle.NoPen)
        x = self.width() / 2
        y = self.height() / 2
        rect = QRectF(x - 10, y - 2, 20, 4)
        painter.drawRoundedRect(rect, 2, 2)
