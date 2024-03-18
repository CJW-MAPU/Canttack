import pandas

from tqdm import tqdm
from random import randint

from common.Type import DataType, AttackType
from module.utils import get_base_timestamp, get_interval
from module.utils import json_parser
from service.AttackService import AttackService
from exception import ExceptionController


class FDAttackService(AttackService):
    __FD_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Flg', 'Dir', 'Payload', 'label']
    __HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    __DLC = ['8', '10', '18', '20']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_dos(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
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
    def make_fuzzing(cls, dataset: pandas.DataFrame):
        attack_data = pandas.DataFrame(columns = cls.__FD_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)

        for i in tqdm(range(0, 1000), leave = True):
            id_data = cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)]
            dlc = cls.__DLC[randint(0, 3)]
            can_id = '00000{0}'.format(id_data)
            payload = [cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)] for _ in range(0, int(dlc, 16))]

            base_timestamp += 0.0001
            attack_data.loc[i, 'Timestamp'] = base_timestamp
            attack_data.loc[i, 'ID'] = can_id
            attack_data.loc[i, 'DLC'] = dlc
            attack_data.loc[i, 'Flg'] = 'FB'
            attack_data.loc[i, 'Dir'] = 'R'
            attack_data.loc[i, 'Payload'] = ' '.join(payload)
            attack_data.loc[i, 'label'] = 1

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset

    @classmethod
    def make_replay(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        data = json_parser(filepath = filepath, data_type = DataType.FD.value, attack_type = AttackType.REPLAY.value)
        base_timestamp = get_base_timestamp(dataset = dataset)

        try:
            attack_data = pandas.read_csv(f'{data["path"]}')
        except KeyError:
            raise ExceptionController.CallInvalidJSONFileException()

        timestamp_diff = attack_data['Timestamp'].diff().fillna(0).tolist()

        for i in range(1, len(timestamp_diff)):
            timestamp_diff[i] += timestamp_diff[i - 1]

        attack_data['Timestamp'] = pandas.DataFrame(columns = ['Timestamp'], data = timestamp_diff) + base_timestamp
        attack_data['label'] = [1 for _ in range(len(attack_data))]

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset

    @classmethod
    def make_spoofing(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
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
