from dataclasses import dataclass, field
from typing import List


@dataclass
class StartUpConfig:
    enable: bool = True
    account_name: str = ""


@dataclass
class FightConfig:
    enable: bool = True
    stage: str = ''
    stone: int = 0
    times: int = 0
    medicine: int = 0


@dataclass
class RecruitConfig:
    enable: bool = True
    refresh: bool = True
    select: List[int] = field(default_factory=lambda: [4, 5, 6])
    confirm: List[int] = field(default_factory=lambda: [4, 5, 6])
    times: int = 0
    expedite: bool = False


@dataclass
class InfrastConfig:
    enable: bool = True
    confirm: List[int] = field(default_factory=list)
    drones: str = '_NotUse'


@dataclass
class TaskConfig:
    startup: StartUpConfig
    fight: FightConfig
    recruit: RecruitConfig
    infrast: InfrastConfig

    @classmethod
    def of(
            cls,
            startup=StartUpConfig(),
            fight=FightConfig(),
            recruit=RecruitConfig(),
            infrast=InfrastConfig()
    ):
        return cls(startup, fight, recruit, infrast)
