__author__ = 'Jae Woong Choi'
__dept__ = 'Hacking and Countermeasure Research Lab in Department of Information Security, Korea University'
__contact__ = 'c.j.biz.woong@gmail.com'
__status__ = '2022-iitp-automobile'
__version__ = '1.0.0'

from module import utils, descriptions

import typing
import pandas
import os

NORMAL_FILE_NAME = '/normal_run_data.csv'
DDOS_FILE_NAME = '/ddos_run_data.csv'
FUZZING_FILE_NAME = '/fuzzing_run_data.csv'


class DatasetFactory:
    """
    This class is create to CAN attack dataset based on attack scenario.
    The input_data parameter of the constructor method must have the following format:
    ::: Timestamp: 1479121434.850202        ID: 0100    000    DLC: 8    00 00 00 00 00 00 00 00 :::

    :@todo: Refactoring
    """

    __directory = None
    __can_column = ['Timestamp', 'ID', 'DLC', 'Payload']

    @classmethod
    def __init__(cls, input_data: typing.TextIO):
        """
        :param input_data: raw data ( CAN )
        """
        cls.__directory = os.path.realpath(os.path.curdir) + '/data'
        cls.__before_process(input_data)

    @classmethod
    def __before_process(cls, input_data: typing.TextIO) -> None:
        """
        :param input_data: raw data ( CAN )
        """
        target = cls.__directory + NORMAL_FILE_NAME

        if not os.path.exists(cls.__directory):
            descriptions.print_directory_is_not_exists(cls.__directory)
            os.makedirs(cls.__directory)

        if not os.path.exists(target):
            descriptions.print_normal_dataset_is_not_exists(target)
            cls.__create_can_normal_dataset(input_data, target)
            # return cls.__txt_to_dataframe(input_data, path)
        else:
            descriptions.print_normal_dataset_is_exists(target)

    @classmethod
    def __create_can_normal_dataset(cls, input_data: typing.TextIO, target: str) -> None:
        """
        :param input_data: raw data ( CAN )
        :param target: absolute path about dataset
        """
        dataframe = pandas.read_csv(input_data, sep = '   ', header = None)
        dataframe = dataframe.drop([1, 3], axis = 1)
        dataframe.columns = cls.__can_column
        dataframe['Timestamp'] = dataframe['Timestamp'].str[11:]
        dataframe['ID'] = dataframe['ID'].str[6:]
        dataframe['DLC'] = dataframe['DLC'].str[6:]
        dataframe['Payload'] = dataframe['Payload'].str[1:]

        dataframe.to_csv(target, sep = ',', index = False)

    @classmethod
    def __get_normal_dataset(cls) -> pandas.DataFrame:
        """
        :return: Normal Dataset.
        """
        target = cls.__directory + NORMAL_FILE_NAME

        if not os.path.exists(target):
            raise FileNotFoundError('Normal Dataset Not Found!')
        else:
            return pandas.read_csv(target)

    @classmethod
    def print_normal_dataset_info(cls):
        dataset = cls.__get_normal_dataset().sort_values('Timestamp')

        print(f'Minimum Timestamp Value : {dataset["Timestamp"].min()}')
        print(f'Maximum Timestamp Value : {dataset["Timestamp"].max()}')

    @classmethod
    def fuzzing_builder(cls):
        return cls.__Builder('fuzzing', cls.__get_normal_dataset())

    @classmethod
    def ddos_builder(cls):
        return cls.__Builder('ddos', cls.__get_normal_dataset())

    class __Builder:
        __type: str = ''
        __dataset: pandas.DataFrame = None

        @classmethod
        def __init__(cls, attack_type: str, dataset: pandas.DataFrame):
            cls.__type = attack_type
            cls.__dataset = dataset

        @classmethod
        def add_attack(cls) -> type:
            if cls.__type == 'fuzzing':
                cls.__dataset = utils.make_fuzzing()
                return cls
            elif cls.__type == 'ddos':
                cls.__dataset = utils.make_ddos()
                return cls

        @classmethod
        def build(cls) -> None:
            # @todo: __dataset.to_csv() if __type == ddos/fuzzing then ddos.csv/fuzzing.csv
            print('build')

    # @classmethod
    # def __txt_to_dataframe(cls, input_data: typing.TextIO, path: str) -> pandas.DataFrame:
    #     """
    #     :param input_data: raw data ( CAN )
    #     :param path: absolute path about dataset
    #     :return: Normal Dataset
    #     todo: Parallel Processing
    #     """
    #     dataframe = pandas.DataFrame(columns = cls.__can_column)
    #
    #     data = Parallel(n_jobs = multiprocessing.cpu_count(),
    #                     prefer = 'threads')(delayed(lambda line:
    #                                                 pandas.DataFrame([cls.__make_column_data(line)],
    #                                                                  columns = cls.__can_column)
    #                                                 )(line) for line in tqdm(input_data.readlines(), leave = True))
    #
    #     Parallel(n_jobs = multiprocessing.cpu_count(),
    #              prefer = 'threads')(delayed(cls.__concat_dataframe(d)) for d in tqdm(data, leave = True))
    #
    #
    #     return dataframe
    #
    # @classmethod
    # def __concat_dataframe(cls, d) -> None:
    #     cls.__normal_dataset = pandas.concat([cls.__normal_dataset, pandas.DataFrame(d, columns = cls.__can_column)])
    #
    # @classmethod
    # def __make_column_data(cls, line) -> list:
    #     """
    #     :param line: 1 line of raw data ( CAN )
    #     :return: list of data to include in dataset row
    #     """
    #     try:
    #         ary = line.split(' ')
    #         timestamp_idx = ary.index('Timestamp:') + 1
    #         id_idx = ary.index('ID:') + 1
    #         dlc_idx = ary.index('DLC:') + 1
    #
    #         timestamp = ary[timestamp_idx]
    #         _id = ary[id_idx]
    #         dlc = ary[dlc_idx]
    #         payload_idx = -int(dlc)
    #         payload = ary[payload_idx:]
    #         payload[-1] = payload[-1][0:2]
    #         payload = ' '.join(payload)
    #
    #         return [timestamp, _id, dlc, payload, 0]
    #     except ValueError:
    #         return [None, None, None, None, 10]
