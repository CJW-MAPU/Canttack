import pandas
from tqdm import tqdm

from common.Type import DataType, AttackType
from module.utils import get_base_timestamp, get_interval
from module.utils import json_parser
from service.AttackService import AttackService
from exception import ExceptionController


class FDAttackService(AttackService):
    __FD_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Flg', 'Dir', 'Payload', 'label']
    __HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_dos(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        # @todo : [추후] FD 에 dos 주입 구현
        attack_data = pandas.DataFrame(columns = cls.__FD_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)
        data = json_parser(filepath = filepath, data_type = DataType.FD.value, attack_type = AttackType.DOS.value)

        try:
            for i in tqdm(range(0, 4000), leave = True):
                base_timestamp += 0.00025
                attack_data.loc[i, 'Timestamp'] = base_timestamp
                attack_data.loc[i, 'ID'] = data['id']
                attack_data.loc[i, 'DLC'] = data['dlc']
                attack_data.loc[i, 'Flg'] = data['flg']
                attack_data.loc[i, 'Dir'] = data['dir']
                attack_data.loc[i, 'Payload'] = data['payload']
                attack_data.loc[i, 'label'] = 1
        except KeyError:
            raise ExceptionController.CallInvalidJSONFileException()

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset

    @classmethod
    def make_fuzzing(cls, dataset: pandas.DataFrame):  # -> pandas.DataFrame:
        # @todo : [추후] FD 에 fuzzing 주입 구현
        raise ExceptionController.CallNotSupportServiceException(data_type = DataType.FD.value,
                                                                 attack_type = AttackType.FUZZING.value)
        pass

    @classmethod
    def make_replay(cls, dataset: pandas.DataFrame, filepath: str):  # -> pandas.DataFrame:
        # @todo : [1순위] FD 에 replay 주입 구현
        raise ExceptionController.CallNotSupportServiceException(data_type = DataType.FD.value,
                                                                 attack_type = AttackType.REPLAY.value)
        pass

    @classmethod
    def make_spoofing(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        # @todo : [1순위] FD 에 spoofing 주입 구현
        attack_data = pandas.DataFrame(columns = cls.__FD_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)
        data = json_parser(filepath = filepath, data_type = DataType.FD.value, attack_type = AttackType.SPOOFING.value)

        try:
            for i in tqdm(range(0, 1000), leave = True):
                base_timestamp += 0.0001
                attack_data.loc[i, 'Timestamp'] = base_timestamp
                attack_data.loc[i, 'ID'] = data['id']
                attack_data.loc[i, 'DLC'] = data['dlc']
                attack_data.loc[i, 'Flg'] = data['flg']
                attack_data.loc[i, 'Dir'] = data['dir']
                attack_data.loc[i, 'Payload'] = data['payload']
                attack_data.loc[i, 'label'] = 1
        except KeyError:
            raise ExceptionController.CallInvalidJSONFileException()

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset
