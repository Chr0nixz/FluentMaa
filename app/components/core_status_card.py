from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import CardWidget, IconWidget, TitleLabel, SubtitleLabel, ProgressBar, PrimaryPushButton, \
    FluentIcon, PushButton, BodyLabel, InfoBadge, InfoBadgePosition, TransparentPushButton, IndeterminateProgressBar

from app.common.extra_icon import ExtraIcon
from app.common.maa.core.maa_core import maaCore
from app.common.resource_manager import resource
from app.common.signal_bus import signalBus


class CoreStatusCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(350, 280)

        self.iconWidget = IconWidget(QIcon(resource.getImg('maa_logo.png')))
        self.titleLabel = TitleLabel(self.tr('Maa Core'))
        self.subLabel = BodyLabel(self.tr('Status') + ' :')
        self.statusLabel =BodyLabel(self.tr('Checking update'))
        self.progressBar = IndeterminateProgressBar(self)
        self.reloadButton = PrimaryPushButton(FluentIcon.SYNC, self.tr('Reload Maa'), self)
        self.detailButton = PushButton(FluentIcon.MENU, self.tr('Running Instances'), self)
        self.verLabel = BodyLabel(self.tr('version') + ' :')
        self.versionLabel = BodyLabel()

        self.vBoxLayout = QVBoxLayout()
        self.statusLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.versionLayout = QHBoxLayout()

        self.initWidget()
        self.connectSignalToSlot()

    def initWidget(self):
        font = self.subLabel.font()
        font.setPixelSize(18)
        self.subLabel.setFont(font)
        self.statusLabel.setFont(font)
        self.statusLabel.setTextColor(QColor('#2aacb8'), QColor('#2aacb8'))
        self.iconWidget.setFixedSize(100, 100)
        self.verLabel.hide()
        self.versionLabel.hide()
        self.reloadButton.setEnabled(False)

        self.initLayout()

    def initLayout(self):
        self.statusLayout.addWidget(self.subLabel)
        self.statusLayout.addWidget(self.statusLabel)

        self.buttonLayout.addWidget(self.reloadButton)
        self.buttonLayout.addWidget(self.detailButton)

        self.versionLayout.addWidget(self.verLabel, 0)
        self.versionLayout.addWidget(self.versionLabel, 1)

        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.setContentsMargins(24, 16, 24, 16)
        self.vBoxLayout.setSpacing(8)
        self.vBoxLayout.addWidget(self.iconWidget, 1)
        self.vBoxLayout.addWidget(self.titleLabel, 1)
        self.vBoxLayout.addLayout(self.statusLayout, 1)
        self.vBoxLayout.addWidget(self.progressBar, 1)
        self.vBoxLayout.addLayout(self.versionLayout, 0)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)

    def connectSignalToSlot(self):
        signalBus.maaCoreStatus.connect(self.changeStatus)
        signalBus.maaCoreLoaded.connect(self.onCoreLoaded)

    def changeStatus(self, status: int):
        match status:
            case 0:
                self.statusLabel.setText(self.tr('Stop'))
                self.statusLabel.setTextColor(QColor('#b54747'), QColor('#b54747'))
            case 1:
                self.statusLabel.setText(self.tr('Running'))
                self.statusLabel.setTextColor(QColor('#4e8752'), QColor('#4e8752'))
                self.versionLabel.setText(maaCore.getVersion())
                self.progressBar.hide()
                self.verLabel.show()
                self.versionLabel.show()
            case 2:
                self.statusLabel.setText(self.tr('Updating'))
                self.statusLabel.setTextColor(QColor('#2aacb8'), QColor('#2aacb8'))
            case 3:
                self.statusLabel.setText(self.tr('Loading'))
                self.statusLabel.setTextColor(QColor('#2aacb8'), QColor('#2aacb8'))

    def onCoreLoaded(self, success):
        if success[0] == 2:
            self.warningButton = TransparentPushButton(ExtraIcon.WARNING, self.tr('Warning'), self)
            self.statusLayout.addWidget(self.warningButton)
            print(self.warningButton.styleSheet())

