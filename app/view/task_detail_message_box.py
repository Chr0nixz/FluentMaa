from dataclasses import asdict

from qfluentwidgets import MessageBoxBase

from app.common.maa.config.maa_task_config import StartUpConfig, FightConfig, RecruitConfig, InfrastConfig
from app.components.task_setting_views.fight_setting_view import FightSettingView
from app.components.task_setting_views.infrast_setting_view import InfrastSettingView
from app.components.task_setting_views.recruit_setting_view import RecruitSettingView
from app.components.task_setting_views.startup_setting_view import StartUpSettingView


class TaskDetailMessageBox(MessageBoxBase):
    def __init__(self,  index: int,  task: dict,  parent=None):
        super().__init__(parent)
        self.index = index
        self.type = task['type']

        match self.type:
            case 'StartUp':
                self.task = StartUpConfig(**task['config'])
                w = StartUpSettingView(self).getWidget(self.task)
            case 'Fight':
                self.task = FightConfig(**task['config'])
                w = FightSettingView(self).getWidget(self.task)
            case 'Recruit':
                self.task = RecruitConfig(**task['config'])
                w = RecruitSettingView(self).getWidget(self.task)
            case 'Infrast':
                self.task = InfrastConfig(**task['config'])
                w = InfrastSettingView(self).getWidget(self.task)

        w.submitButton.hide()
        w.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.addWidget(w)

        self.widget.setMinimumSize(500, 600)

    def getTask(self):
        print(asdict(self.task))
        return {'type': self.type, 'config': asdict(self.task)}
