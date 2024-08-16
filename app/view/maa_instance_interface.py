from PySide6.QtCore import Qt
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import TitleLabel, PushButton, FluentIcon, PrimaryPushButton, ScrollArea, FlowLayout, CommandBar, \
    Action, LargeTitleLabel, InfoBar, InfoBarPosition, CheckableMenu, MenuIndicatorType, TransparentDropDownPushButton

from app.common import windows_manager
from app.common.maa.config.maa_config_manager import maaConfig
from app.common.maa.config.maa_connection_config import ConnectionConfig
from app.common.maa.config.maa_instance_config import InstanceConfig
from app.common.style_sheet import StyleSheet
from app.components.maa_instance_card import MaaInstanceCard, MaaInstanceCardView
from app.view.add_instance_message_box import AddInstanceMessageBox


class ToolBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.editing = False

        self.titleLabel = LargeTitleLabel(self.tr('MAA Instances'), self)

        self.commandBar = CommandBar()

        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(130)

        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.addAction(Action(FluentIcon.ADD, self.tr('Add'), triggered=self.parent().addInstance))
        self.commandBar.addAction(Action(FluentIcon.SYNC, self.tr('Refresh'), triggered=self.parent().loadCards))
        self.commandBar.addSeparator()
        self.commandBar.addAction(Action(
            FluentIcon.EDIT,
            self.tr('Edit'),
            checkable=True,
            triggered=self.switchEdit
        ))
        self.commandBar.addSeparator()
        self.cardLayoutAction = Action(FluentIcon.TILES, self.tr('Card'), checkable=True)
        self.listLayoutAction = Action(FluentIcon.MENU, self.tr('List'), checkable=True)
        self.layoutActionGroup = QActionGroup(self)
        self.layoutActionGroup.addAction(self.cardLayoutAction)
        self.layoutActionGroup.addAction(self.listLayoutAction)
        self.cardLayoutAction.setChecked(True)
        self.layoutMenu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)
        self.layoutMenu.addActions([self.cardLayoutAction, self.listLayoutAction])
        self.layoutButton = TransparentDropDownPushButton(self.tr('Layout'), self, FluentIcon.LAYOUT)
        self.layoutButton.setMenu(self.layoutMenu)
        self.commandBar.addWidget(self.layoutButton)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.commandBar, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)


    def switchEdit(self):
        if self.editing:
            self.parent().maaInstanceCardView.hideRemove()
            self.editing = False
        else:
            self.parent().maaInstanceCardView.showRemove()
            self.editing = True


class MaaInstanceInterface(ScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('maaInstanceInterface')

        self.selectedCards = []

        StyleSheet.MAA_INSTANCE_INTERFACE.apply(self)

        self.view = QWidget(self)
        self.toolBar = ToolBar(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidgets()
        self.loadCards()

    def __initWidgets(self):

        self.view.setObjectName('view')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(30, 20, 30, 36)

    def addInstance(self):
        w = AddInstanceMessageBox(windows_manager.main_window)
        if w.exec():
            connection = ConnectionConfig(address=w.addressInput.text(), emulator=w.emulatorInput.currentData())
            self.loadCard(maaConfig.addInstance(InstanceConfig(name=w.nameInput.text(), connection=connection)))

    def loadCards(self):
        if hasattr(self, 'maaInstanceCardView'):
            self.vBoxLayout.removeWidget(self.maaInstanceCardView)
            self.maaInstanceCardView.setParent(None)
            self.maaInstanceCardView.deleteLater()
        self.maaInstanceCardView = MaaInstanceCardView(self)
        windows_manager.main_window.stackedWidget.currentChanged.connect(self.maaInstanceCardView.update)
        for instance in maaConfig.getInstances().items():
            self.maaInstanceCardView.addCard(MaaInstanceCard(self, instance[0], instance[1]))
        self.vBoxLayout.addWidget(self.maaInstanceCardView)
        self.vBoxLayout.update()
        self.selectedCards.clear()

    def loadCard(self, instance: dict):
        self.maaInstanceCardView.addCard(MaaInstanceCard(self, instance[0], instance[1]))
        self.maaInstanceCardView.update()

    def selectCard(self, card):
        if self.toolBar.editing:
            pass
        else:
            if self.selectedCards:
                self.selectedCards[0].unselect()
                self.selectedCards[0] = card
            else:
                self.selectedCards.append(card)
        w = InfoBar.info(
            title=self.tr('Current Selection'),
            content=self.tr('Instance ') + str(card),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=2000,
            parent=self.parent()
        )

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
