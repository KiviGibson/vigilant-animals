from enum import Enum


class PlayerAction(Enum):
    NoAction = 0
    Pass = 1
    UnitCardPlayed = 2
    BurstCardPlayed = 3
    SlowCardPlayed = 4
