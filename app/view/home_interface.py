from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QLinearGradient, QColor, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import FluentIcon, ScrollArea, isDarkTheme

from app.common.resource_manager import resource
from app.common.style_sheet import StyleSheet
from app.components.card_flow_view import CardFlowView
from app.components.core_status_card import CoreStatusCard
from app.components.link_card import LinkCardView


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.maaLabel = QLabel('MAA GUI', self)
        self.banner = QPixmap(':/images/home_header.png')
        self.linkCardView = LinkCardView(self)

        self.maaLabel.setObjectName('maaLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.maaLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.linkCardView.addCard(
            resource.getImg('maa_logo.png'),
            self.tr('MAA Instances'),
            self.tr('Click to switch to the instance management interface'),
            'maaInstanceInterface'
        )

        self.linkCardView.addCard(
            FluentIcon.SETTING,
            self.tr('Settings'),
            self.tr('Manage application settings, include MAA settings, personalization, etc.'),
            'settingInterface'
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.panelWidget = CardFlowView(self.tr('Panel'), self)
        self.panelWidget.addCard(CoreStatusCard(self))

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.addWidget(self.panelWidget)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def emerge(self):
        pass

