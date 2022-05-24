import typing
import os
import binascii
import pandas
import numpy as np
import random

from tqdm import tqdm

COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload']


def make_fuzzing(dataset: pandas.DataFrame) -> pandas.DataFrame:
    attack_data = pandas.DataFrame(columns = COLUMNS)
    base_timestamp = get_base_timestamp(dataset = dataset)

    for i in tqdm(range(0, 10), leave = True):
        id_data = binascii.b2a_hex(os.urandom(15)).decode('utf-8')
        payload_data = binascii.b2a_hex(os.urandom(15)).decode('utf-8')
        payload = list()
        dlc = random.randint(3, 8)

        for j in range(1, dlc + 1):
            temp = j * 2
            payload.append(payload_data[temp - 2:temp])

        base_timestamp += 0.0000001
        attack_data.loc[i, 'Timestamp'] = base_timestamp
        attack_data.loc[i, 'ID'] = '0{0}'.format(id_data[0:3])
        attack_data.loc[i, 'DLC'] = str(dlc)
        attack_data.loc[i, 'Payload'] = ' '.join(payload)
        attack_data.loc[i, 'label'] = 1

    dataset = pandas.concat([dataset, attack_data])

    dataset = dataset.sort_values(by = 'Timestamp')

    return dataset


def make_ddos(dataset: pandas.DataFrame) -> pandas.DataFrame:
    attack_data = pandas.DataFrame(columns = COLUMNS)
    base_timestamp = get_base_timestamp(dataset = dataset)

    for i in tqdm(range(0, 100), leave = True):
        base_timestamp += 0.0000001
        attack_data.loc[i, 'Timestamp'] = base_timestamp
        attack_data.loc[i, 'ID'] = '015b'
        attack_data.loc[i, 'DLC'] = '8'
        attack_data.loc[i, 'Payload'] = 'ff ff ff ff ff ff ff ff'
        attack_data.loc[i, 'label'] = 1

    dataset = pandas.concat([dataset, attack_data])

    dataset = dataset.sort_values(by = 'Timestamp')

    return dataset


def get_base_timestamp(dataset: pandas.DataFrame) -> float:
    return dataset['Timestamp'].tolist()[random.randint(0, len(dataset) - 1)]


def create_can_normal_dataset(input_data: typing.TextIO, target: str) -> None:
    """
    :param input_data: raw data ( CAN )
    :param target: absolute path about dataset
    """

    dataframe = pandas.read_csv(input_data, sep = '   ', header = None, engine = 'python')
    dataframe = dataframe.drop([1, 3], axis = 1)
    dataframe.columns = COLUMNS
    dataframe['Timestamp'] = dataframe['Timestamp'].str[11:]
    dataframe['ID'] = dataframe['ID'].str[6:]
    dataframe['DLC'] = dataframe['DLC'].str[6:]
    dataframe['Payload'] = dataframe['Payload'].str[1:]

    temp = np.array([0 for i in range(0, len(dataframe))])
    dataframe['label'] = temp
    dataframe = dataframe.drop([len(dataframe) - 1], axis = 0)
    dataframe.to_csv(f'{target}.csv', sep = ',', index = False)

    print(f'File creating is success.')
    print(f'File path is {os.getcwd()}/{target}.csv')
