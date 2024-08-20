from dataclasses import dataclass


@dataclass
class ConnectionConfig:
    address: str
    emulator: str
