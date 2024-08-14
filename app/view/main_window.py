from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow, SplashScreen, NavigationItemPosition

from app.common.signal_bus import signalBus
from app.view.home_interface import HomeInterface
from app.view.maa_instance_interface import MaaInstanceInterface
from app.view.setting_interface import SettingInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.homeInterface = HomeInterface(self)
        self.maaInstanceInterface = MaaInstanceInterface(self)
        self.settingInterface = SettingInterface(self)

        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        self.initNavigation()

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)

        self.setWindowTitle('MaaAssistantArknights')
        self.setWindowIcon(QIcon(':/images/maa_logo.png'))

        self.setMicaEffectEnabled(True)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.maaInstanceInterface, FIF.APPLICATION, self.tr('Instances'), pos)

        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def connectSignalToSlot(self):
        signalBus.switchToInterface.connect(self.switchToInterface)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToInterface(self, route_key):
        interfaces = self.findChildren(QWidget)
        for w in interfaces:
            if w.objectName() == route_key:
                self.stackedWidget.setCurrentWidget(w, False)
