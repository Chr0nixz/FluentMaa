from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):

    switchToInterface = Signal(str)
    instanceChanged = Signal(str)
    taskListChanged = Signal()
    taskListAdded = Signal()
    taskListRemoved = Signal(tuple)
    taskSettingClicked = Signal(str)

    maaCoreStatus = Signal(int)
    maaCoreLoaded = Signal(tuple)
    maaCoreUpdated = Signal()
    maaCoreUnready = Signal()
    instanceStatusChanged = Signal(int)
    instanceStop = Signal(str)

    instanceMessage = Signal(tuple)
    poolMessage = Signal(tuple)


signalBus = SignalBus()
