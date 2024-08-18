from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from qfluentwidgets import SegmentedWidget, ScrollArea, ExpandLayout, SettingCardGroup, PrimaryPushButton

from app.common.maa.maa_instance_manager import maaInstanceManager
from app.common.style_sheet import StyleSheet


class TaskSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.submitButton = PrimaryPushButton(self)
        self.submitButton.setText(self.tr('Add'))
        self.submitButton.clicked.connect(lambda: maaInstanceManager.addTaskCur(self.taskType))
        self.submitButton.setFixedWidth(160)

    def addSubInterface(self, widget: QWidget, name: str, text: str):
        widget.setObjectName(name)
        self.stackedWidget.addWidget(widget)

        self.nav.addItem(
            routeKey=name,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.nav.setCurrentItem(widget.objectName())

    def build(self):
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.nav.setCurrentItem('basicInterface')

        StyleSheet.TASK_SETTING_VIEW.apply(self)

        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)
        self.vBoxLayout.addWidget(self.nav, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addWidget(self.submitButton, alignment=Qt.AlignmentFlag.AlignCenter)
        return self


class TaskSettingInterface(ScrollArea):
    def __init__(self, parent=None, title=None):
        super().__init__(parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.settingGroup = SettingCardGroup(title, self.scrollWidget)

        self.initWidget()

    def initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')

    def initLayout(self):
        self.expandLayout.addWidget(self.settingGroup)

    def addCard(self, card):
        self.settingGroup.addSettingCard(card)

