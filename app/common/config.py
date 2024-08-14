import sys
from enum import Enum

from PySide6.QtCore import QLocale
from qfluentwidgets import ConfigSerializer, QConfig, ConfigItem, BoolValidator, Theme, qconfig, OptionsConfigItem, \
    OptionsValidator


class Language(Enum):
    """ 语言枚举 """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English, QLocale.UnitedStates)
    AUTO = QLocale(QLocale.Chinese, QLocale.China)


class LanguageSerializer(ConfigSerializer):
    """ 语言序列化 """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ 设置类 """
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config/config.json', cfg)
