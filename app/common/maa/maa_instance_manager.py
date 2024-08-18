from dataclasses import asdict

from app.common.maa.config.maa_config_manager import maaConfig
from app.common.maa.maa_instance import MaaInstance
from app.common.signal_bus import signalBus


class MaaInstanceManager:
    def __init__(self):
        self.instances = {}
        self.current = None
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
        self.addTask(self.current.uid, taskType)

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


maaInstanceManager = MaaInstanceManager()
