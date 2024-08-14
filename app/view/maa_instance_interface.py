from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import TitleLabel, PushButton, FluentIcon, PrimaryPushButton, ScrollArea, FlowLayout, CommandBar, \
    Action

from app.common import windows_manager
from app.common.style_sheet import StyleSheet
from app.components.maa_instance_card import MaaInstanceCard, MaaInstanceCardView
from app.view.add_instance_message_box import AddInstanceMessageBox


class ToolBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.titleLabel = TitleLabel(self.tr('MAA Instances'), self)

        self.commandBar = CommandBar()

        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(110)

        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.addAction(Action(FluentIcon.ADD, self.tr('Add'), triggered=self.addInstance))
        self.commandBar.addSeparator()
        self.commandBar.addAction(Action(FluentIcon.EDIT, self.tr('Edit'), triggered=lambda: print("编辑")))
        print(self.commandBar.suitableWidth())

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.commandBar, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def addInstance(self):
        w = AddInstanceMessageBox(windows_manager.main_window)
        if w.exec():
            print('ok')


class MaaInstanceInterface(ScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('maaInstanceInterface')

        StyleSheet.MAA_INSTANCE_INTERFACE.apply(self)

        self.view = QWidget(self)
        self.toolBar = ToolBar(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidgets()
        self.__loadCards()

    def __initWidgets(self):
        self.view.setObjectName('view')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(30, 20, 30, 36)


    def __loadCards(self):
        maaInstanceCardView = MaaInstanceCardView()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        maaInstanceCardView.addCard()
        self.vBoxLayout.addWidget(maaInstanceCardView)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
