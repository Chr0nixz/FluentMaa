from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QSplitter, QSplitterHandle
from qfluentwidgets import isDarkTheme


class VerticalSplitter(QSplitter):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
        VerticalSplitter::handle:vertical:hover {
            background-color: rgb(227, 229, 232)
        }
        VerticalSplitter::handle:vertical:click {
            background-color: rgb(219, 221, 224)
        }
        """)

    def createHandle(self):
        return VerticalSplitterHandle(self.orientation(), self)


class VerticalSplitterHandle(QSplitterHandle):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme:
            painter.setBrush(QBrush(QColor("#a1a1a1")))
        else:
            painter.setBrush(QBrush(QColor("#818181")))
        painter.setPen(Qt.PenStyle.NoPen)
        x = self.width() / 2
        y = self.height() / 2
        rect = QRectF(x - 10, y - 2, 20, 4)
        painter.drawRoundedRect(rect, 2, 2)
