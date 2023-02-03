from enum import Enum


class AttackType(Enum):
    DOS = 'dos'
    FUZZING = 'fuzzing'
    REPLAY = 'replay'
    SPOOFING = 'spoofing'


class DataType(Enum):
    CAN = 'can'
    FD = 'can-fd'
    AE = 'automotive-ethernet'
