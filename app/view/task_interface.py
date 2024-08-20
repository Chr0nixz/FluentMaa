from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QListWidget
from qfluentwidgets import LargeTitleLabel, StrongBodyLabel, TransparentDropDownPushButton, RoundMenu, Action, \
    MessageBox, ListWidget

from app.common import windows_manager
from app.common.maa.emulators import Emulator
from app.common.maa.instance.maa_instance_manager import maaInstanceManager
from app.common.resource_manager import resource
from app.common.signal_bus import signalBus
from app.components.separator_widget import VerticalSeparatorWidget
from app.components.splitter import VerticalSplitter
from app.components.task_list import TaskListView
from app.components.task_setting_views.task_setting_widget import TaskSettingWidget


class ToolBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.instance = self.parent().instance

        self.titleLabel = LargeTitleLabel(self.tr('Basic Task'), self)
        self.currentLabel = StrongBodyLabel(self.tr('Current instance') + ': ', self)
        self.currentButton = TransparentDropDownPushButton(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(130)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(16)

        self.hBoxLayout.addWidget(self.currentLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.currentButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def updateWidget(self):
        self.instance = self.parent().instance
        self.currentMenu = RoundMenu(self)
        self.currentMenu.addAction(Action(Emulator.getIcon(self.instance.connection.emulator), self.instance.name))
        self.currentButton.setMenu(self.currentMenu)
        self.currentButton.setText(self.instance.name)


class TaskWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.instance = self.parent().instance

        self.taskOptions = ListWidget()
        self.separator = VerticalSeparatorWidget(self)
        self.taskSettingWidget = TaskSettingWidget(parent=self)
        self.taskListView = TaskListView(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        startUpItem = QListWidgetItem(self.tr('StartUp'))
        startUpItem.setIcon(QIcon(resource.getImg('maa_logo.png')))
        startUpItem.setData(0, 'StartUp')
        fightItem = QListWidgetItem(self.tr('Fight'))
        fightItem.setIcon(QIcon(resource.getImg('maa_logo.png')))
        fightItem.setData(0, 'Fight')
        self.taskOptions.addItem(startUpItem)
        self.taskOptions.addItem(fightItem)
        self.taskOptions.itemClicked.connect(lambda i: self.taskSettingWidget.switchWidget(i.data(0)))
        self.taskOptions.setDragEnabled(True)
        self.taskOptions.setAcceptDrops(True)
        self.taskOptions.setDragDropMode(QListWidget.DragDropMode.InternalMove)

    def __initLayout(self):
        self.splitter = VerticalSplitter(self)
        self.splitter.addWidget(self.taskOptions)
        self.splitter.addWidget(self.taskListView)
        self.splitter.setSizes([1, 1])
        self.vBoxLayout.addWidget(self.splitter)

        self.hBoxLayout.addLayout(self.vBoxLayout, 1)
        self.hBoxLayout.addWidget(self.separator)
        self.hBoxLayout.addWidget(self.taskSettingWidget, 2)

    def updateWidget(self):
        if not self.instance == maaInstanceManager.current:
            self.instance = maaInstanceManager.current
            signalBus.taskListChanged.emit()
            self.hBoxLayout.removeWidget(self.taskSettingWidget)
            self.taskSettingWidget.setParent(None)
            self.taskSettingWidget.deleteLater()
            self.taskSettingWidget = TaskSettingWidget(parent=self)
            self.hBoxLayout.addWidget(self.taskSettingWidget, 2)
            self.taskListView.taskList.clear()
            self.taskListView.taskList.loadTasks()


class TaskInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.instance = maaInstanceManager.current

        self.setObjectName('taskInterface')

        self.toolBar = ToolBar(self)
        self.taskWidget = TaskWidget(self)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.toolBar)
        self.vBoxLayout.addWidget(self.taskWidget)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.vBoxLayout)


    def emerge(self):
        self.instance = maaInstanceManager.current
        if self.instance:
            self.toolBar.updateWidget()
            self.taskWidget.updateWidget()
        else:
            w = MessageBox(self.tr('No selected instance'),
                           self.tr('Click OK to switch to the instance interface to select one.'),
                           windows_manager.main_window)
            w.cancelButton.hide()
            if w.exec():
                signalBus.switchToInterface.emit('maaInstanceInterface')
