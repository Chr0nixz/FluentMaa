from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):

    switchToInterface = Signal(str)
    instanceChanged = Signal(str)
    taskListChanged = Signal()
    taskListAdded = Signal()
    taskListRemoved = Signal(tuple)
    taskSettingClicked = Signal(str)

    maaCoreStatus = Signal(int)
    maaCoreLoaded = Signal(bool)
    maaCoreUpdated = Signal()
    maaCoreUnready = Signal()
    instanceStatusChanged = Signal(int)

    instanceMessage = Signal(tuple)
    poolMessage = Signal(tuple)


signalBus = SignalBus()
