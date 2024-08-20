import importlib
import json
import os.path
from enum import Enum

from PySide6.QtCore import QThread

from app.common.config import cfg
from app.common.maa.asst import asst
from app.common.maa.asst.asst import Asst
from app.common.maa.asst.updater import Updater
from app.common.maa.asst.utils import Version, Message
from app.common.signal_bus import signalBus
from app.common.threads import threads, mutex


class LoadThread(QThread):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        importlib.reload(asst)
        signalBus.maaCoreLoaded.emit(asst.Asst.load(self.path))


class UpdateThread(QThread):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        updater = Updater(self.path, Version.Stable)
        updater.update()


class UpdateLoadThread(QThread):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.updater = None

    def run(self):
        try:
            mutex.lock()
            updater = Updater(self.path, Version.Nightly)
            self.updater = updater
            self.updater.update()
            importlib.reload(asst)
            signalBus.maaCoreLoaded.emit(asst.Asst.load(self.path))
            mutex.unlock()
        except Exception as e:
            print(e)


class MaaCore:
    class Status(Enum):
        STOP = 0
        RUNNING = 1
        UPDATING = 2
        LOADING = 3

    def __init__(self):
        self.status = MaaCore.Status.STOP
        self.path = cfg.maaFolder.value

        signalBus.maaCoreLoaded.connect(self._onMaaCoreLoaded)

    def init(self, update=True):
        if not os.path.isfile(os.path.join(self.path, 'MaaCore.dll')):
            self.setStatus(MaaCore.Status.STOP)
            return
        if update:
            threads.addThreadRun(UpdateLoadThread(self.path))
        else:
            pass

    def setStatus(self, status: Status):
        self.status = status
        signalBus.maaCoreStatus.emit(status.value)
        if self.status == MaaCore.Status.STOP:
            signalBus.maaCoreLoaded.emit(False)

    def _onMaaCoreLoaded(self, loaded):
        if loaded:
            self.setStatus(MaaCore.Status.RUNNING)
        else:
            pass


@Asst.CallBackType
def printCallback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))

    print(m, d, arg)

@Asst.CallBackType
def signalCallback(msg, details, arg):
    m = Message(msg)
    d = json.loads(details.decode('utf-8'))
    signalBus.instanceMessage.emit((m, d))

maaCore = MaaCore()
