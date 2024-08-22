from qfluentwidgets import FluentIcon

from app.common.maa.config.maa_task_config import RecruitConfig
from app.components.setting_cards.spin_box_setting_card import SpinBoxSettingCard
from app.components.task_setting_views.task_setting_view import TaskSettingView, TaskSettingInterface


class RecruitSettingView:
    def __init__(self, parent):
        self.parent = parent
        self.taskType = 'Recruit'

    def getWidget(self, config: RecruitConfig):
        view = TaskSettingView(self.parent)
        view.taskType = self.taskType
        view.config = config
        basicInterface = TaskSettingInterface(self.parent, self.parent.tr('Recruit Basic'))
        basicInterface.addCard(
            SpinBoxSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Max times')
            )
        )
        basicInterface.initLayout()
        view.addSubInterface(basicInterface, 'basicInterface', self.parent.tr('Basic Settings'))
        return view.build()
