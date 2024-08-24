from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor


class ExtraIcon(FluentIconBase, Enum):

    WARNING = 'warning'

    def path(self, theme=Theme.AUTO) -> str:
        return f':/svg/{self.value}_{getIconColor(theme).lower()}.svg'

