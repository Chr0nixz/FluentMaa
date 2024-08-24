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
    facility: List[int] = field(default_factory=lambda: ["Mfg", "Trade", "Power", "Control", "Reception", "Office", "Dorm"])
    drones: str = '_NotUse'
    threshold: float = 0.3


@dataclass
class MallConfig:
    enable: bool = True
    shopping: bool = True


@dataclass
class AwardConfig:
    enable: bool = True
    award: bool = True
    mail: bool = True
    recruit: bool = False
    orundum: bool = False
    mining: bool = False


@dataclass
class TaskConfig:
    startup: StartUpConfig
    fight: FightConfig
    recruit: RecruitConfig
    infrast: InfrastConfig
    mall: MallConfig
    award: AwardConfig

    @classmethod
    def of(
            cls,
            startup=StartUpConfig(),
            fight=FightConfig(),
            recruit=RecruitConfig(),
            infrast=InfrastConfig(),
            mall=MallConfig(),
            award=AwardConfig()
    ):
        return cls(startup, fight, recruit, infrast, mall, award)
