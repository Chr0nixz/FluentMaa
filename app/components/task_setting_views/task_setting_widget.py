from PySide6.QtWidgets import QStackedWidget

from app.common.maa.config.maa_task_config import TaskConfig
from app.common.maa.instance.maa_instance_manager import maaInstanceManager
from app.common.signal_bus import signalBus
from app.components.task_setting_views.fight_setting_view import FightSettingView
from app.components.task_setting_views.recruit_setting_view import RecruitSettingView
from app.components.task_setting_views.startup_setting_view import StartUpSettingView


class TaskSettingWidget(QStackedWidget):
    def __init__(self, config: TaskConfig = None, parent=None):
        super().__init__(parent)
        self.widgets = {}
        if not config:
            if maaInstanceManager.current:
                config = maaInstanceManager.current.task
        if config:
            self.addWidget(StartUpSettingView(self).getWidget(config.startup))
            self.addWidget(FightSettingView(self).getWidget(config.fight))
            self.addWidget(RecruitSettingView(self).getWidget(config.recruit))
        signalBus.taskSettingClicked.connect(self.switchWidget)

    def addWidget(self, w):
        super().addWidget(w)
        self.widgets[w.taskType] = w

    def switchWidget(self, taskType: str):
        self.setCurrentWidget(self.widgets[taskType])
