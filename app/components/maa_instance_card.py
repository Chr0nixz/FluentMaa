from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import IconWidget, ToolButton, FluentIcon, FlowLayout, PrimaryToolButton, Dialog, InfoBar, \
    InfoBarPosition, ElevatedCardWidget

from app.common import windows_manager
from app.common.config import cfg
from app.common.maa.config.maa_config_manager import maaConfig
from app.common.maa.emulators import Emulator
from app.common.resource_manager import resource
from app.common.style_sheet import StyleSheet
from app.view.instance_detail_message_box import InstanceDetailMessageBox


class MaaInstanceCard(ElevatedCardWidget):
    def __init__(self, interface, instance_id: int, instance_config: dict):
        super().__init__()
        self.interface = interface

        self.id = instance_id
        self.config = instance_config

        self.name = self.config['name']
        self.emulator = self.config['connection']['emulator']
        self.address = self.config['connection']['address']
        self.status = 'Stop'
        self.warnings = []
        self.view = None
        self.setProperty('checked', False)

        self.setFixedSize(240, 300)
        self.iconWidget = IconWidget(
            Emulator.getIcon(self.emulator, default=QIcon(resource.getImg('maa_logo.png'))),
            parent=self
        )
        self.titleLabel = QLabel(self.name, self)
        content = f'{self.tr('Address')}: {self.address}\n{self.tr('Status')}: {self.status}\n'
        if not self.warnings:
            content += self.tr('No warning')
        self.contentLabel = QLabel(content, self)
        self.startButton = PrimaryToolButton(FluentIcon.PLAY, self)
        self.stopButton = PrimaryToolButton(FluentIcon.PAUSE, self)
        self.removeButton = ToolButton(FluentIcon.DELETE, self)
        self.detailWidget = IconWidget(FluentIcon.MORE, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidgets()
        self.__connectSignalToSlot()

    def __initWidgets(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(100, 100)
        self.detailWidget.setFixedSize(16, 16)

        self.removeButton.hide()

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(20, 25, 20, 15)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addSpacing(12)

        self.vBoxLayout.addLayout(self.buttonLayout, 1)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.addWidget(self.startButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.stopButton, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(3)
        self.buttonLayout.addWidget(self.removeButton, 0, Qt.AlignRight)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.detailWidget, 0, Qt.AlignRight)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.startButton.setObjectName('startButton')
        self.stopButton.setObjectName('stopButton')
        self.removeButton.setObjectName('removeButton')

    def __connectSignalToSlot(self):
        self.removeButton.clicked.connect(self.removeConfirm)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.property('selected'):
            self.clickSelected()
        else:
            self.select()

    def removeConfirm(self):
        w = Dialog(self.tr('Are you sure to remove the instance?'),
                   self.tr('If you remove the instance, it will disappear from the list foverver.\n' +
                           'But you can backup config/maa.json to recover data.'),
                   windows_manager.main_window)
        w.yesButton.setText(self.tr('Remove'))
        w.cancelButton.setText(self.tr('Cancel'))
        if w.exec():
            self.remove()

    def select(self):
        self.setProperty('selected', True)
        self.parent().update()
        self.interface.selectCard(self)

    def clickSelected(self):
        w = InstanceDetailMessageBox(windows_manager.main_window, self.config)
        if w.exec():
            pass
        self.parent().update()

    def unselect(self):
        self.setProperty('selected', False)
        self.parent().update()

    def remove(self):
        self.parent().removeCard(self)
        maaConfig.removeInstance(self.id)
        self.setParent(None)
        self.deleteLater()

    def __str__(self):
        return self.name + ': ' + self.address


class MaaInstanceCardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.flowLayout = FlowLayout(self, True)

        self.flowLayout.setContentsMargins(20, 10, 20, 20)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(15)
        self.flowLayout.setAlignment(Qt.AlignLeft)

        StyleSheet.MAA_INSTANCE_CARD.apply(self)
        color = cfg.themeColor.value
        self.add_style_light = f'''
            MaaInstanceCard[selected=true] {{
                border: 2px solid rgba({color.red()}, {color.green()}, {color.blue()}, 0.9);
                border-radius: 10px;
                background-color: rgba(249, 249, 249, 0.95);
            }}

            MaaInstanceCard[selected=true]:hover {{
                background-color: rgba(249, 249, 249, 0.93);
                border: 2px solid rgba({color.red()}, {color.green()}, {color.blue()}, 0.85);
            }}
        '''
        self.add_style_dark = f'''
            MaaInstanceCard[selected=true] {{
                border: 2px solid rgba({color.red()}, {color.green()}, {color.blue()}, 0.9);
                border-radius: 10px;
                background-color: rgba(39, 39, 39, 0.95);
            }}

            MaaInstanceCard[selected=true]:hover {{
                background-color: rgba(39, 39, 39, 0.93);
                border: 2px solid rgba({color.red()}, {color.green()}, {color.blue()}, 0.85);
            }}
        '''

    def addCard(self, card):
        """ add link card """
        self.flowLayout.addWidget(card)
        card.view = self

    def showRemove(self):
        for card in self.findChildren(MaaInstanceCard):
            card.removeButton.show()
            card.update()

    def hideRemove(self):
        for card in self.findChildren(MaaInstanceCard):
            card.removeButton.hide()
            card.update()

    def removeCard(self, card):
        self.flowLayout.removeWidget(card)
        w = InfoBar.warning(
            title=self.tr('Removed'),
            content=self.tr('Instance: ') + str(card),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=3000,
            parent=self.parent()
        )
        self.update()

    def update(self):
        super().update()
        if cfg.theme.value == "Dark":
            self.setStyleSheet(self.styleSheet() + self.add_style_dark)
        elif cfg.theme.value == "Light":
            self.setStyleSheet(self.styleSheet() + self.add_style_light)