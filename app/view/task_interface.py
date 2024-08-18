from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QSplitter
from qfluentwidgets import LargeTitleLabel, StrongBodyLabel, TransparentDropDownPushButton, RoundMenu, Action, \
    MessageBox, ListWidget

from app.common import windows_manager
from app.common.maa.emulators import Emulator
from app.common.maa.maa_instance_manager import maaInstanceManager
from app.common.resource_manager import resource
from app.common.signal_bus import signalBus
from app.components.separator_widget import VerticalSeparatorWidget, HorizontalSeparatorWidget
from app.components.splitter import VerticalSplitter
from app.components.task_list_view import TaskListView
from app.components.task_setting_views.fight_setting_view import FightSettingView
from app.components.task_setting_views.startup_setting_view import StartUpSettingView


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

    def updateData(self):
        self.instance = self.parent().instance
        self.currentMenu = RoundMenu(self)
        self.currentMenu.addAction(Action(Emulator.getIcon(self.instance.connection.emulator), self.instance.name))
        self.currentButton.setMenu(self.currentMenu)
        self.currentButton.setText(self.instance.name)


class TaskWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.taskList = ListWidget()
        self.separator = VerticalSeparatorWidget(self)
        self.view = StartUpSettingView(self).getWidget(None)
        self.taskListView = TaskListView()

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
        self.taskList.addItem(startUpItem)
        self.taskList.addItem(fightItem)
        self.taskList.itemClicked.connect(self.parent().switchTask)

    def __initLayout(self):
        splitter = VerticalSplitter(self)
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.addWidget(self.taskList)
        splitter.addWidget(self.taskListView)
        self.vBoxLayout.addWidget(splitter)
        #self.vBoxLayout.addWidget(self.taskList, 3)
        #self.vBoxLayout.addWidget(HorizontalSeparatorWidget(self))
        #self.vBoxLayout.addWidget(self.taskListView, 2)

        self.hBoxLayout.addLayout(self.vBoxLayout, 1)
        self.hBoxLayout.addWidget(self.separator)
        self.hBoxLayout.addWidget(self.view, 2)

    def switchView(self, view):
        self.hBoxLayout.removeWidget(self.view)
        self.view.setParent(None)
        self.view.deleteLater()
        self.view = view
        self.hBoxLayout.addWidget(self.view, 2)

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

    def __initWidget(self):
        pass

    def emerge(self):
        self.instance = maaInstanceManager.current
        print(self.instance)
        if self.instance:
            self.toolBar.updateData()
            signalBus.taskListChanged.emit()
        else:
            w = MessageBox(self.tr('No selected instance'),
                           self.tr('Click OK to switch to the instance interface to select one.'),
                           windows_manager.main_window)
            w.cancelButton.hide()
            if w.exec():
                signalBus.switchToInterface.emit('maaInstanceInterface')

    def switchTask(self, item):
        if not item.data(0) == self.taskWidget.view.taskType:
            match item.data(0):
                case 'StartUp':
                    self.taskWidget.switchView(StartUpSettingView(self).getWidget(self.instance.task.startup))
                case 'Fight':
                    print(type(self.instance.task.fight))
                    self.taskWidget.switchView(FightSettingView(self).getWidget(self.instance.task.fight))
