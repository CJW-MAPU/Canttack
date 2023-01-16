import pandas

from tqdm import tqdm
from service.AttackService import AttackService
from module.utils import get_base_timestamp, get_interval
from random import randint


class FDAttackService(AttackService):
    __FD_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Flg', 'Dir', 'Payload', 'label']
    __HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_dos(cls, dataset: pandas.DataFrame) -> pandas.DataFrame:
        # @todo : [추후] FD 에 dos 주입 구현
        pass

    @classmethod
    def make_fuzzing(cls, dataset: pandas.DataFrame) -> pandas.DataFrame:
        # @todo : [추후] FD 에 fuzzing 주입 구현
        pass

    @classmethod
    def make_replay(cls, dataset: pandas.DataFrame) -> pandas.DataFrame:
        # @todo : [1순위] FD 에 replay 주입 구현
        pass

    @classmethod
    def make_spoofing(cls, dataset: pandas.DataFrame) -> pandas.DataFrame:
        # @todo : [1순위] FD 에 spoofing 주입 구현

        attack_data = pandas.DataFrame(columns = cls.__FD_COLUMNS)
        base_timestamp = get_base_timestamp(dataset = dataset)
        # @         todo : end_timestamp 기준 잡기
        end_timestamp = base_timestamp

        i = 0
        with tqdm() as pbar:
            while base_timestamp < end_timestamp:
                pbar.update(1)
                id_data = None  # @todo : id 값 가져 오기
                dlc = None  # @todo : dlc 가져 오기
                flg = None  # @todo : flg 가져 오기
                _dir = None # @todo : dir 가져 오기
                fd_id = '00000{0}'.format(id_data)
                interval = get_interval(identifier = fd_id, dataset = dataset)
                payload = None  # @todo : payload 가져 오기

                base_timestamp += interval
                attack_data.loc[i, 'Timestamp'] = base_timestamp
                attack_data.loc[i, 'ID'] = fd_id
                attack_data.loc[i, 'DLC'] = dlc
                attack_data.loc[i, 'Flg'] = flg
                attack_data.loc[i, 'Dir'] = _dir
                attack_data.loc[i, 'Payload'] = ' '.join(payload)
                attack_data.loc[i, 'label'] = 1

        dataset = pandas.concat([dataset, attack_data])

        dataset = dataset.sort_values(by = 'Timestamp')

        return dataset
