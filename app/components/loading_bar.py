from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QSize, QEvent, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QFrame
from qfluentwidgets import InfoBar, InfoBarPosition, TransparentToolButton, FluentIcon, FluentStyleSheet, TextWrap, \
    InfoBarManager, isDarkTheme

from app.common.signal_bus import signalBus
from app.common.style_sheet import StyleSheet
from app.components.loading_label import LoadingLabel


class LoadingBar(QFrame):
    closedSignal = Signal()

    def __init__(
            self,
            title: str,
            content: str,
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=None
    ):
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.orient = orient
        self.isClosable = isClosable
        self.position = position

        self.iconWidget = LoadingLabel(self)
        self.titleLabel = QLabel(self)
        self.contentLabel = QLabel(self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.textLayout = QHBoxLayout() if self.orient == Qt.Horizontal else QVBoxLayout()
        self.widgetLayout = QHBoxLayout() if self.orient == Qt.Horizontal else QVBoxLayout()

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni = QPropertyAnimation(
            self.opacityEffect, b'opacity', self)

        self.lightBackgroundColor = None
        self.darkBackgroundColor = None

        signalBus.maaCoreLoaded.connect(lambda i: self.__fadeOut())
        signalBus.maaCoreStatus.connect(self.setStatus)

        self.__initWidget()

    def __initWidget(self):
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.closeButton.setFixedSize(36, 36)
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.setVisible(self.isClosable)

        self.__setQss()
        self.__initLayout()

        self.closeButton.clicked.connect(self.close)

    def __initLayout(self):
        self.hBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.textLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.textLayout.setAlignment(Qt.AlignTop)
        self.textLayout.setContentsMargins(1, 8, 0, 8)

        self.hBoxLayout.setSpacing(0)
        self.textLayout.setSpacing(5)

        # add icon to layout
        self.hBoxLayout.addSpacing(8)
        self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(16)

        # add title to layout
        self.textLayout.addWidget(self.titleLabel, 1, Qt.AlignTop)
        self.titleLabel.setVisible(bool(self.title))

        # add content label to layout
        if self.orient == Qt.Horizontal:
            self.textLayout.addSpacing(7)

        self.textLayout.addWidget(self.contentLabel, 1, Qt.AlignTop)
        self.contentLabel.setVisible(bool(self.content))
        self.hBoxLayout.addLayout(self.textLayout)

        # add widget layout
        if self.orient == Qt.Horizontal:
            self.hBoxLayout.addLayout(self.widgetLayout)
            self.widgetLayout.setSpacing(10)
        else:
            self.textLayout.addLayout(self.widgetLayout)

        # add close button to layout
        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignLeft)

        self._adjustText()

    def setStatus(self, status: int):
        print(status)
        if status == 2:
            self.title = self.tr('Updating Maa')
            self._adjustText()
        elif status == 3:
            self.title = self.tr('Loading Maa')
            self._adjustText()

    def __setQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.setProperty('type', 'Info')

        StyleSheet.LOADING_BAR.apply(self)

    def __fadeOut(self):
        self.opacityAni.setDuration(200)
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.finished.connect(self.close)
        self.opacityAni.start()

    def _adjustText(self):
        w = 900 if not self.parent() else (self.parent().width() - 50)

        # adjust title
        chars = max(min(w / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        # adjust content
        chars = max(min(w / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])
        self.adjustSize()

    def addWidget(self, widget: QWidget, stretch=0):
        self.widgetLayout.addSpacing(6)
        align = Qt.AlignTop if self.orient == Qt.Vertical else Qt.AlignVCenter
        self.widgetLayout.addWidget(widget, stretch, Qt.AlignLeft | align)

    def setCustomBackgroundColor(self, light, dark):
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() in [QEvent.Resize, QEvent.WindowStateChange]:
                self._adjustText()

        return super().eventFilter(obj, e)

    def closeEvent(self, e):
        self.closedSignal.emit()
        self.deleteLater()

    def showEvent(self, e):
        self._adjustText()
        super().showEvent(e)

        if self.position != InfoBarPosition.NONE:
            manager = InfoBarManager.make(self.position)
            manager.add(self)

        if self.parent():
            self.parent().installEventFilter(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.lightBackgroundColor is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if isDarkTheme():
            painter.setBrush(self.darkBackgroundColor)
        else:
            painter.setBrush(self.lightBackgroundColor)

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 6, 6)
