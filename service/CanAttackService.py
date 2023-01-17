import pandas

from tqdm import tqdm
from random import randint

from service.AttackService import AttackService
from module.utils import get_base_timestamp, json_parser
from common.Type import DataType, AttackType
from exception import ExceptionController


class CanAttackService(AttackService):
    __CAN_COLUMNS = CAN_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload', 'label']
    __HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_dos(cls, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        attack_data = pandas.DataFrame(columns = cls.__CAN_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)
        data = json_parser(filepath = filepath, data_type = DataType.CAN.value, attack_type = AttackType.DOS.value)

        try:
            for i in tqdm(range(0, 4000), leave = True):
                base_timestamp += 0.00025
                attack_data.loc[i, 'Timestamp'] = base_timestamp
                attack_data.loc[i, 'ID'] = data['id']
                attack_data.loc[i, 'DLC'] = data['dlc']
                attack_data.loc[i, 'Payload'] = data['payload']
                attack_data.loc[i, 'label'] = 1
        except KeyError:
            raise ExceptionController.CallInvalidJSONFileException()

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset

    @classmethod
    def make_fuzzing(cls, dataset: pandas.DataFrame) -> pandas.DataFrame:
        attack_data = pandas.DataFrame(columns = cls.__CAN_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)

        for i in tqdm(range(0, 1000), leave = True):
            id_data = cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)]
            dlc = randint(3, 8)
            can_id = '00000{0}'.format(id_data)
            payload = [cls.__HEX[randint(0, 15)] + cls.__HEX[randint(0, 15)] for _ in range(0, dlc)]

            base_timestamp += 0.0001
            attack_data.loc[i, 'Timestamp'] = base_timestamp
            attack_data.loc[i, 'ID'] = can_id
            attack_data.loc[i, 'DLC'] = str(dlc)
            attack_data.loc[i, 'Payload'] = ' '.join(payload)
            attack_data.loc[i, 'label'] = 1

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset
        pass

    def make_replay(self, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        # @todo : [추후] CAN 에 replay 주입 구현
        pass

    def make_spoofing(self, dataset: pandas.DataFrame, filepath: str) -> pandas.DataFrame:
        # @todo : [추후] CAN 에 replay 주입 구현
        pass
