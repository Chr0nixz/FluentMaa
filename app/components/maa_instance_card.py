from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import IconWidget, ToolButton, FluentIcon, FlowLayout, PrimaryToolButton

from app.common.resource_manager import resource
from app.common.style_sheet import StyleSheet
from app.view.add_instance_message_box import AddInstanceMessageBox


class MaaInstanceCard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedSize(240, 300)
        self.iconWidget = IconWidget(QIcon(resource.getImg('maa_logo.png')), self)
        self.titleLabel = QLabel('1', self)
        self.contentLabel = QLabel('address', self)
        self.startButton = PrimaryToolButton(FluentIcon.PLAY, self)
        self.stopButton = PrimaryToolButton(FluentIcon.PAUSE, self)
        self.removeButton = ToolButton(FluentIcon.DELETE, self)
        self.detailWidget = IconWidget(FluentIcon.MORE, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidgets()

    def __initWidgets(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(100, 100)
        self.detailWidget.setFixedSize(16, 16)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(20, 25, 20, 15)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.vBoxLayout.addLayout(self.buttonLayout, 1)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.addWidget(self.startButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.stopButton, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(3)
        self.buttonLayout.addWidget(self.removeButton, 0, Qt.AlignRight)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.detailWidget, 0, Qt.AlignRight)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.startButton.setObjectName('startButton')
        self.stopButton.setObjectName('stopButton')
        self.removeButton.setObjectName('removeButton')


class MaaInstanceCardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flowLayout = FlowLayout(self, True)

        self.flowLayout.setContentsMargins(20, 10, 20, 20)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(15)
        self.flowLayout.setAlignment(Qt.AlignLeft)

        StyleSheet.MAA_INSTANCE_CARD.apply(self)

    def addCard(self):
        """ add link card """
        card = MaaInstanceCard(self)
        self.flowLayout.addWidget(card)
