from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QMovie, QPixmap, QPainter
from PySide6.QtWidgets import QLabel

from app.common.resource_manager import resource


class LoadingLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie(resource.getGif('loading.gif'))
        self.pixmap = QPixmap()
        self.movie.frameChanged.connect(self.update_frame)
        self.setFixedSize(20, 20)

        self.movie.start()

    def update_frame(self):
        frame = self.movie.currentPixmap()
        scaled_frame = frame.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_frame)
