from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import FlowLayout, SubtitleLabel

from app.common.maa.maa_instance_manager import maaInstanceManager
from app.common.signal_bus import signalBus
from app.components.task_card import TaskCard


class TaskListView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.cards = []

        self.titleLabel = SubtitleLabel(self.tr('Task List'))

        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout(needAni=True)
        self.loadTaskList()
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addLayout(self.flowLayout)
        self.setLayout(self.vBoxLayout)

        signalBus.taskListChanged.connect(self.loadTaskList)
        signalBus.taskListAdded.connect(self.addTask)

    def loadTaskList(self):
        self.flowLayout.removeAllWidgets()
        self.count = 0
        for card in self.cards:
            card.setParent(None)
            card.deleteLater()
        if maaInstanceManager.current:
            for task in maaInstanceManager.current.task_list:
                self.addTask(task)

    def addTask(self, task: dict):
        card = TaskCard(self.count, task, self)
        self.flowLayout.addWidget(card)
        self.cards.append(card)
        self.count += 1
