from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget
from qfluentwidgets import isDarkTheme


class VerticalSeparatorWidget(QWidget):

    def __init__(self, parent=None, width=9):
        super().__init__(parent=parent)
        self.setFixedWidth(width)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(3)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class HorizontalSeparatorWidget(QWidget):

    def __init__(self, parent=None, height=9):
        super().__init__(parent=parent)
        self.setFixedHeight(height)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(3)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        y = self.height() // 2
        painter.drawLine(0, y, self.width(), y)

