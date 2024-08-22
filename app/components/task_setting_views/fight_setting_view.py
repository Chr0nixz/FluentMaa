from qfluentwidgets import FluentIcon

from app.common.maa.config.maa_task_config import FightConfig
from app.components.setting_cards.input_setting_card import InputSettingCard
from app.components.setting_cards.spin_box_setting_card import SpinBoxSettingCard
from app.components.setting_cards.switch_button_setting_card import SwitchButtonSettingCard
from app.components.task_setting_views.task_setting_view import TaskSettingView, TaskSettingInterface


class FightSettingView:
    def __init__(self, parent):
        self.parent = parent
        self.taskType = 'Fight'

    def getWidget(self, config: FightConfig):
        view = TaskSettingView(self.parent)
        view.taskType = self.taskType
        view.config = config
        basicInterface = TaskSettingInterface(self.parent, self.parent.tr('Fight Basic'))
        basicInterface.addCard(
            InputSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Stage'),
                config=config,
                name='stage'
            )
        )
        basicInterface.addCard(
            SpinBoxSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Medicine Number'),
                config=config,
                name='medicine'
            )
        )
        basicInterface.addCard(
            SpinBoxSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Stone Number'),
                config=config,
                name='stone'
            )
        )
        basicInterface.addCard(
            SpinBoxSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Times'),
                config=config,
                name='times'
            )
        )
        basicInterface.initLayout()
        view.addSubInterface(basicInterface, 'basicInterface', self.parent.tr('Basic Settings'))
        advanceInterface = TaskSettingInterface(self.parent, self.parent.tr('Fight Advanced'))
        advanceInterface.addCard(
            SwitchButtonSettingCard(
                icon=FluentIcon.SETTING,
                title=self.parent.tr('Use residual san')
            )
        )
        advanceInterface.initLayout()
        view.addSubInterface(advanceInterface, 'advanceInterface', self.parent.tr('Advanced Settings'))
        return view.build()
