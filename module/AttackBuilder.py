import pandas

from module.utils import make_fuzzing, make_ddos


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
    def add_attack(cls):
        if cls.__attack_type == 'fuzzing':
            # cls.__dataset = make_fuzzing(dataset = cls.__dataset)
            print('fuzzing')
        elif cls.__attack_type == 'ddos':
            # cls.__dataset = make_ddos(dataset = cls.__dataset)
            print('ddos')

    @classmethod
    def build(cls) -> None:
        # @todo: __dataset.to_csv() if __type == ddos/fuzzing then ddos.csv/fuzzing.csv
        print('build')
