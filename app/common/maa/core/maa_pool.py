import os.path
import queue
import time

from PySide6.QtCore import QThread, QTimer

from app.common.config import cfg
from app.common.maa.asst.asst import Asst
from app.common.maa.core.maa_core import printCallback, signalCallback
from app.common.maa.instance.maa_instance import MaaInstance, InstanceStatus
from app.common.signal_bus import signalBus
from app.common.threads import threads


class MaaPool:
    def __init__(self):
        self.queue = queue.Queue()

    def init(self):
        signalBus.maaCoreLoaded.connect(self.start)

    def start(self):
        self.thread = MaaPoolThread(self.queue)
        threads.addThreadRun(self.thread)

    def add(self, instance):
        self.queue.put(instance)

class MaaPoolThread(QThread):
    def __init__(self, queue: queue.Queue):
        super().__init__()
        self.queue = queue
        self.asstList = []

    def run(self):
        while True:
            print(self.queue)
            if not self.queue.empty():
                instance = self.queue.get()
                self.addInstance(instance)
            print(self.asstList)
            if self.asstList:
                for i in self.asstList:
                    print(i.running())
                    if not i.running():
                        i.instance.setStatus(InstanceStatus.STOP)
                        self.asstList.remove(i)
                print(self.asstList)
            time.sleep(1)

    def addInstance(self, instance: MaaInstance):
        asst = Asst(callback=printCallback)
        if asst.connect(os.path.join(cfg.maaFolder.value, 'adb/platform-tools/adb.exe'),
                        instance.connection.address):
            print('s')
        for task in instance.task_list:
            asst.append_task(task['type'], task['config'])
        asst.instance = instance
        signalBus.instanceStop.connect(asst.stopByUid)
        asst.start()
        self.asstList.append(asst)
        signalBus.instanceMessage.emit((instance.uid, 'start', True))
        instance.setStatus(InstanceStatus.RUNNING)


maaPool = MaaPool()
