from dataclasses import asdict

from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QListWidgetItem, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ListWidget, StrongBodyLabel, TransparentPushButton, TransparentToolButton, FluentIcon, \
    SubtitleLabel

from app.common import windows_manager
from app.common.maa.instance.maa_instance_manager import maaInstanceManager
from app.common.signal_bus import signalBus
from app.view.task_detail_message_box import TaskDetailMessageBox


class TaskListWidget(ListWidget):
    def __init__(self, tasks: list = None, parent=None):
        super().__init__(parent)
        if not tasks:
            if maaInstanceManager.current:
                tasks = maaInstanceManager.current.task_list
        self.tasks = tasks
        self.connectSignalToSlot()
        self.loadTasks()

    def loadTasks(self):
        if maaInstanceManager.current:
            self.tasks = maaInstanceManager.current.task_list
        if self.tasks:
            for task in self.tasks:
                self.addTask(task=task)

    def addTask(self, index: int = None, task: dict = None):
        if not index:
            index = self.count()
        if not task:
            task = maaInstanceManager.current.task_list[-1]
        item = QListWidgetItem()
        self.addItem(item)
        self.setItemWidget(item, TaskItemWidget(index, task, item))

    def removeTask(self, index: int):
        self.takeItem(index)
        self.refreshIndex()

    def refreshIndex(self):
        for i in range(self.count()):
            self.itemWidget(self.item(i)).setIndex(i)

    def connectSignalToSlot(self):
        signalBus.taskListRemoved.connect(lambda t: self.removeTask(t[0]))
        signalBus.taskListAdded.connect(self.addTask)


class TaskItemWidget(QWidget):

    def __init__(self, index: int, task: dict, item: QListWidgetItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.index = index
        self.task = task

        self.indexLabel = StrongBodyLabel(str(index + 1), self)
        self.taskButton = TransparentPushButton(task['type'], self)
        self.removeButton = TransparentToolButton(
            FluentIcon.CLOSE.colored(QColor(0, 0, 0, 15), QColor(255, 255, 255, 21)), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(12, 0, 8, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.addWidget(self.indexLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.taskButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.removeButton, alignment=Qt.AlignmentFlag.AlignRight)

        self.taskButton.clicked.connect(self.showDetail)
        self.removeButton.clicked.connect(self.remove)

        self.setLayout(self.hBoxLayout)

    def setIndex(self, index: int):
        self.index = index
        self.indexLabel.setText(str(index + 1))

    def remove(self):
        signalBus.taskListRemoved.emit((self.index, self.task))

    def showDetail(self):
        w = TaskDetailMessageBox(self.index, self.task, windows_manager.main_window)
        if w.exec():
            maaInstanceManager.updateTaskCur(w.index, w.getTask())
            self.refreshTask()

    def refreshTask(self):
        self.task = maaInstanceManager.getTaskCur(self.index)


class TaskListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.titleLabel = SubtitleLabel(self.tr('Task list'))
        self.taskList = TaskListWidget()
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.taskList)
