import pandas
import os

from module.utils import make_fuzzing, make_dos


class AttackBuilder:
    __attack_type: str = None
    __dataset: pandas.DataFrame = None

    @classmethod
    def __init__(cls, dataset_name: str):
        cls.__dataset = pandas.read_csv(f'{dataset_name}.csv')

    @classmethod
    def set_attack_type(cls, attack_type: str):
        cls.__attack_type = attack_type

    @classmethod
    def inject_attack(cls):
        if cls.__attack_type == 'fuzzing':
            cls.__dataset = make_fuzzing(dataset = cls.__dataset)
        elif cls.__attack_type == 'dos':
            cls.__dataset = make_dos(dataset = cls.__dataset)
        elif cls.__attack_type == 'replay':
            pass
            # @todo : Implement replay attack inject
            # cls.__dataset = make_replay(dataset = cls.__dataset)
        elif cls.__attack_type == 'spoofing':
            pass
            # @todo : Implement spoofing attack inject
            # cls.__dataset = make_spoofing(dataset = cls.__dataset)

    @classmethod
    def build(cls) -> None:
        cls.__dataset.to_csv(f'{cls.__attack_type}_run_data.csv', sep = ',', index = False)
        print()
        print(f'File creating is success.')
        print(f'File path is {os.getcwd()}/{cls.__attack_type}_run_data.csv')
