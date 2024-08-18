from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentWindow, SplashScreen, NavigationItemPosition

from app.common import windows_manager
from app.common.resource_manager import resource
from app.common.signal_bus import signalBus
from app.view.home_interface import HomeInterface
from app.view.maa_instance_interface import MaaInstanceInterface
from app.view.setting_interface import SettingInterface
from app.view.task_interface import TaskInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        windows_manager.main_window = self

        self.homeInterface = HomeInterface(self)
        self.maaInstanceInterface = MaaInstanceInterface(self)
        self.taskInterface = TaskInterface(self)
        self.settingInterface = SettingInterface(self)

        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        self.initNavigation()

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)

        self.setWindowTitle('MaaAssistantArknights')
        self.setWindowIcon(QIcon(resource.getImg('gui_logo.png')))

        self.setMicaEffectEnabled(True)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(250, 250))
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
        self.addSubInterface(self.taskInterface, FIF.CHECKBOX, self.tr('Basic Task'), pos)

        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def connectSignalToSlot(self):
        signalBus.switchToInterface.connect(self.switchToInterface)
        self.stackedWidget.currentChanged.connect(lambda: self.stackedWidget.currentWidget().emerge())


    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToInterface(self, route_key):
        interfaces = self.findChildren(QWidget)
        for w in interfaces:
            if w.objectName() == route_key:
                self.stackedWidget.setCurrentWidget(w, False)
