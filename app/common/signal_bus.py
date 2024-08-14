from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    switchToInterface = Signal(str)


signalBus = SignalBus()
