from qfluentwidgets import FluentIcon

from app.common.maa.config.maa_task_config import InfrastConfig
from app.components.setting_cards.multi_combobox_setting_view import MultiComboBoxSettingCard
from app.components.task_setting_views.task_setting_view import TaskSettingView, TaskSettingInterface


class InfrastSettingView:
    def __init__(self, parent):
        self.parent = parent
        self.taskType = 'Infrast'

    def getWidget(self, config: InfrastConfig):
        view = TaskSettingView(self.parent)
        view.taskType = self.taskType
        view.config = config
        basicInterface = TaskSettingInterface(self.parent, self.parent.tr('Infrastructure Basic'))
        basicInterface.addCard(
            MultiComboBoxSettingCard(
                icon=FluentIcon.SETTING,
                selections=["Mfg", "Trade", "Power", "Control", "Reception", "Office", "Dorm"],
                title=self.parent.tr('Facility'),
                content=self.parent.tr('Selected all by default'),
                config=config,
                name='facility'
            )
        )
        basicInterface.initLayout()
        view.addSubInterface(basicInterface, 'basicInterface', self.parent.tr('Basic Settings'))
        return view.build()
