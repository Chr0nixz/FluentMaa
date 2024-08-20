import json
import os

from app.common.maa.instance.maa_instance import MaaInstance


def serializer(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    raise TypeError(f"Type {type(obj)} is not serializable")


class MaaConfig:

    def __init__(self, file):
        self.config = {'instances': {}}
        self.file = file
        if not os.path.isdir(os.path.dirname(self.file)):
            os.mkdir(os.path.dirname(self.file))
        self.load()

    def load(self):
        if not os.path.exists(self.file):
            self.config = {'instances': {}}
        try:
            with open(self.file, 'r', encoding='utf-8') as file:
                self.config = json.loads(file.read())
        except FileNotFoundError:
            self.dump()

    def dump(self):
        with open(self.file, 'w+', encoding='utf-8') as file:
            file.write(json.dumps(self.config, default=serializer, indent=4))
            file.seek(0)
            self.config = json.loads(file.read())

    def addInstance(self, instance: MaaInstance):
        self.config['instances'].update({str(instance.uid): instance.__dict__()})
        self.dump()

    def getInstances(self) -> dict:
        return self.config['instances']

    def removeInstance(self, uid):
        self.config['instances'].pop(str(uid))
        self.dump()


maaConfig = MaaConfig(file=os.path.join(os.getcwd(), 'config/maa.json'))
