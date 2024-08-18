import uuid
from dataclasses import fields

from app.common.maa.config.maa_connection_config import ConnectionConfig
from app.common.maa.config.maa_task_config import TaskConfig


class MaaInstance:
    def __init__(
            self,
            uid: int = None,
            name: str = None,
            connection: ConnectionConfig = None,
            config: dict = None
    ):
        self.uid = uid
        if config:
            self.name = config['name']
            self.connection = ConnectionConfig(**config['connection'])
            self.task = from_dict(TaskConfig, config['task'])
            self.task_list = config['task_list']
        else:
            if name:
                self.name = name
            else:
                self.name = connection.emulator
            self.connection = connection
            self.task = TaskConfig.of()
            self.task_list = []

    @classmethod
    def fromConfig(cls, uid: int, config: dict):
        return cls(uid=uid, config=config)

    @classmethod
    def create(cls, name, address, emulator):
        return cls(uid=uuid.uuid4().int, name=name, connection=ConnectionConfig(address, emulator))

    def __dict__(self):
        return {
            'name': self.name,
            'connection': self.connection,
            'task': self.task,
            'task_list': self.task_list
        }


def from_dict(dataclass_type, data):
    fieldtypes = {f.name: f.type for f in fields(dataclass_type)}
    return dataclass_type(
        **{f: from_dict(fieldtypes[f], data[f]) if isinstance(data[f], dict) else data[f] for f in data})
