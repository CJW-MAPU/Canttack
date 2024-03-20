import pandas
import os

from common.Type import AttackType, DataType
from factory.AttackServiceFactory import AttackServiceFactory
from service.AttackService import AttackService
from exception import ExceptionController


class AttackBuilder:
    __attack_type: str = None
    __name: str = None
    __dataset: pandas.DataFrame = None
    __attack_service_factory: AttackServiceFactory = AttackServiceFactory()
    __attack_service: AttackService = None

    @classmethod
    def __init__(cls, dataset_name: str, name: str, data_type: str):
        cls.__dataset = pandas.read_csv(f'{dataset_name}.csv')
        cls.__attack_service = cls.__attack_service_factory.create_service(data_type = data_type)
        cls.__name = name

    @classmethod
    def set_attack_type(cls, attack_type: str):
        cls.__attack_type = attack_type

    @classmethod
    def inject_attack(cls, filepath: str):
        if cls.__attack_type == AttackType.DOS.value:
            cls.__dataset = cls.__attack_service.make_dos(dataset = cls.__dataset, filepath = filepath)
        elif cls.__attack_type == AttackType.FUZZING.value:
            cls.__dataset = cls.__attack_service.make_fuzzing(dataset = cls.__dataset)
        elif cls.__attack_type == AttackType.REPLAY.value:
            cls.__dataset = cls.__attack_service.make_replay(dataset = cls.__dataset, filepath = filepath)
        elif cls.__attack_type == AttackType.SPOOFING.value:
            cls.__dataset = cls.__attack_service.make_spoofing(dataset = cls.__dataset, filepath = filepath)
        else:
            raise ExceptionController.CallNotSupportAttackTypeException()

    @classmethod
    def build(cls) -> None:
        cls.__dataset.to_csv(f'data/{cls.__name}.csv', sep = ',', index = False)
        print()
        print(f'File creating is success.')
        print(f'File path is {os.getcwd()}/data/{cls.__name}.csv')
