import os.path
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig

from app.common.resource_manager import resource


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    LINK_CARD = "link_card"
    HOME_INTERFACE = "home_interface"
    SETTING_INTERFACE = "setting_interface"
    MAA_INSTANCE_INTERFACE = "maa_instance_interface"
    MAA_INSTANCE_CARD = "maa_instance_card"
    TASK_SETTING_VIEW = "task_setting_view"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        path = os.path.join(resource.qss, theme.value.lower(), self.value)
        return path + '.qss'
    