from qfluentwidgets import FluentIcon

from app.components.setting_cards.input_setting_card import InputSettingCard
from app.components.task_setting_views.task_setting_view import TaskSettingView, TaskSettingInterface


class StartUpSettingView:
    def __init__(self, parent):
        self.parent = parent
        self.taskType = 'StartUp'

    def getWidget(self, config):
        view = TaskSettingView(self.parent)
        view.taskType = self.taskType
        view.config = config
        basicInterface = TaskSettingInterface(self.parent, self.parent.tr('Fight'))
        basicInterface.addCard(
            InputSettingCard(
                icon=FluentIcon.PEOPLE,
                title=self.parent.tr('Switch account'),
                config=config,
                name='account_name'
            )
        )
        basicInterface.initLayout()
        view.addSubInterface(basicInterface, 'basicInterface', self.parent.tr('Basic Settings'))
        return view.build()

