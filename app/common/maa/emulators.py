from enum import Enum

from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon


class Emulator(Enum):
    MUMU = 'MuMu Emulator'

    @classmethod
    def getIcon(cls, value: str, default: QIcon = FluentIcon.GAME) -> QIcon:
        value = value.lower().replace(' ', '_')
        icon = QIcon(f':/images/icon/{value}.ico')
        if icon.isNull():
            icon = default
        return icon
