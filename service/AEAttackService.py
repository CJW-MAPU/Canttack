import pandas
from tqdm import tqdm

from service.AttackService import AttackService
from exception import ExceptionController
from common.Type import DataType, AttackType


class AEAttackService(AttackService):

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_dos(cls, dataset: pandas.DataFrame, filepath: str) -> None:
        raise ExceptionController.CallNotSupportAttackServiceException(data_type = DataType.AE.value,
                                                                       attack_type = AttackType.DOS.value)
        pass

    @classmethod
    def make_fuzzing(cls, dataset: pandas.DataFrame) -> None:
        raise ExceptionController.CallNotSupportAttackServiceException(data_type = DataType.AE.value,
                                                                       attack_type = AttackType.FUZZING.value)
        pass

    @classmethod
    def make_replay(cls, dataset: pandas.DataFrame, filepath: str) -> None:
        raise ExceptionController.CallNotSupportAttackServiceException(data_type = DataType.AE.value,
                                                                       attack_type = AttackType.REPLAY.value)
        pass

    @classmethod
    def make_spoofing(cls, dataset: pandas.DataFrame, filepath: str) -> None:
        raise ExceptionController.CallNotSupportAttackServiceException(data_type = DataType.AE.value,
                                                                       attack_type = AttackType.SPOOFING.value)
        pass
