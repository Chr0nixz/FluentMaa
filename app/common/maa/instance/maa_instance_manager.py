from dataclasses import asdict

from app.common.maa.config.maa_config_manager import maaConfig
from app.common.maa.core.maa_core import maaCore, MaaCore
from app.common.maa.core.maa_pool import maaPool
from app.common.maa.instance.maa_instance import MaaInstance
from app.common.signal_bus import signalBus


class MaaInstanceManager:
    def __init__(self):
        self.instances = {}
        self.current = None
        signalBus.taskListRemoved.connect(lambda t: self.removeTaskCur(t[1]))
        self.loadInstances()

    def loadInstances(self):
        instances = maaConfig.getInstances()
        for instance in instances.items():
            self.instances[instance[0]] = MaaInstance.fromConfig(instance[0], instance[1])

    def getInstances(self) -> list[MaaInstance]:
        return [i[1] for i in self.instances.items()]

    def getInstance(self, uid):
        for i in self.instances.items():
            if i[1].uid == uid:
                return i[1]

    def addInstance(self, instance: MaaInstance):
        self.instances[instance.uid] = instance
        maaConfig.addInstance(instance)

    def addTask(self, uid: int, taskType: str):
        instance = self.getInstance(uid)
        add = {
                'type': taskType,
                'config': asdict(getattr(instance.task, taskType.lower()))
            }
        instance.task_list.append(add)
        self.refreshInstance(instance)
        signalBus.taskListAdded.emit(add)

    def addTaskCur(self, taskType: str):
        add = {
            'type': taskType,
            'config': asdict(getattr(self.current.task, taskType.lower()))
        }
        self.current.task_list.append(add)
        self.refreshInstance(self.current)
        signalBus.taskListAdded.emit()

    def removeTask(self, uid: int, task: dict):
        instance = self.getInstance(uid)
        instance.task_list.remove(task)
        self.refreshInstance(instance)

    def removeTaskCur(self, task: dict):
        print(self.current.task_list, task)
        self.current.task_list.remove(task)
        self.refreshInstanceCur()

    def refreshInstance(self, instance):
        maaConfig.addInstance(instance)

    def refreshInstanceByUid(self, uid):
        self.refreshInstance(self.getInstance(uid))

    def refreshInstanceCur(self):
        self.refreshInstance(self.current)

    def removeInstance(self, uid: int):
        self.instances.pop(uid)
        if self.current.uid == uid:
            self.current = None
        maaConfig.removeInstance(uid)

    def startInstanceByUid(self, uid: int) -> bool:
        if maaCore.status == MaaCore.Status.RUNNING:
            instance = self.getInstance(uid)
            maaPool.add(instance)
            return True
        else:
            signalBus.maaCoreUnready.emit()
            return False

    def startInstance(self, instance: MaaInstance) -> bool:
        if maaCore.status == MaaCore.Status.RUNNING:
            maaPool.add(instance)
            return True
        else:
            signalBus.maaCoreUnready.emit()
            return False


maaInstanceManager = MaaInstanceManager()
