__author__ = 'Jae Woong Choi'
__dept__ = 'Hacking and Countermeasure Research Lab in Department of Information Security, Korea University'
__contact__ = 'c.j.biz.woong@gmail.com'
__status__ = '2022-iitp-automobile'
__version__ = '1.0.0'

import multiprocessing
import typing

import numpy as np
import pandas
import os

from multiprocessing import Pool
from tqdm import tqdm
from joblib import Parallel, delayed


class DatasetFactory:
    """
    This class is create to CAN attack dataset based on attack scenario.
    The input_data parameter of the constructor method must have the following format:
    ::: Timestamp: 1479121434.850202        ID: 0100    000    DLC: 8    00 00 00 00 00 00 00 00 :::

    :todo: Refactoring
    """

    attack_type = None
    __can_column = ['Timestamp', 'ID', 'DLC', 'Payload']
    __normal_dataset: pandas.DataFrame = None
    __fuzzing_dataset: pandas.DataFrame = None
    __ddos_dataset: pandas.DataFrame = None

    @classmethod
    def __init__(cls, input_data: typing.TextIO, attack_type = None):
        """
        :param input_data: raw data ( CAN )
        """
        cls.attack_type = attack_type
        cls.__before_process(input_data)

    @classmethod
    def __before_process(cls, input_data: typing.TextIO) -> None:
        """
        :param input_data: raw data ( CAN )
        :return: Normal Dataset
        """
        current_directory = os.path.realpath(os.path.curdir)
        target_directory = current_directory + '/data'
        path = target_directory + '/normal_run_data.csv'

        if not os.path.exists(target_directory):
            print('Directory Not Found.')
            print('Creating Directory. ' + target_directory)
            print()
            os.makedirs(target_directory)

        if not os.path.exists(path):
            print("you don't have normal dataset.")
            print('Creating Dataset. ' + path)
            print()
            # return cls.__txt_to_dataframe(input_data, path)
            cls.__normal_dataset = cls.__create_can_normal_dataset(input_data, path)
        else:
            print('you already have normal dataset.')
            print('Dataset is ' + path)
            print()
            cls.__normal_dataset = pandas.read_csv(path)

    @classmethod
    def __create_can_normal_dataset(cls, input_data: typing.TextIO, path: str) -> pandas.DataFrame:
        """
        :param input_data: raw data ( CAN )
        :param path: absolute path about dataset
        :return: Normal Dataset
        """
        dataframe = pandas.read_csv(input_data, sep = '   ', header = None)
        dataframe = dataframe.drop([1, 3], axis = 1)
        dataframe.columns = cls.__can_column
        dataframe['Timestamp'] = dataframe['Timestamp'].str[11:]
        dataframe['ID'] = dataframe['ID'].str[6:]
        dataframe['DLC'] = dataframe['DLC'].str[6:]
        dataframe['Payload'] = dataframe['Payload'].str[1:]

        dataframe.to_csv(path, sep = ',', index = False)

        return dataframe

    @classmethod
    def fuzzing_builder(cls):
        cls.attack_type = 'fuzzing'
        return cls

    @classmethod
    def ddos_builder(cls):
        cls.attack_type = 'ddos'
        return cls

    @classmethod
    def add_attack(cls):
        if cls.attack_type == 'fuzzing':
            print('1' + cls.attack_type)
        elif cls.attack_type == 'ddos':
            print('2' + cls.attack_type)
        return cls

    @classmethod
    def build(cls) -> None:
        print('build')

    @classmethod
    def get_normal_dataset(cls) -> pandas.DataFrame:
        """
        :return: Normal Dataset.
        """
        return cls.__normal_dataset

    @classmethod
    def get_ddos_dataset(cls) -> pandas.DataFrame:
        """
        :return: DDoS Dataset.
        """
        return cls.__ddos_dataset

    @classmethod
    def get_fuzzing_dataset(cls) -> pandas.DataFrame:
        """
        :return: Fuzzing Dataset.
        """
        return cls.__fuzzing_dataset

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
