from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    switchToInterface = Signal(str)
    taskListChanged = Signal()
    taskListAdded = Signal(dict)


signalBus = SignalBus()
