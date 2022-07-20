import typing
import os
import pandas
import numpy as np
from random import randint
import random

from tqdm import tqdm

COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload']
HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def make_fuzzing(dataset: pandas.DataFrame) -> pandas.DataFrame:
    attack_data = pandas.DataFrame(columns = COLUMNS)
    base_timestamp = get_base_timestamp(dataset = dataset)

    for i in tqdm(range(0, 1000), leave = True):
        id_data = HEX[randint(0, 15)] + HEX[randint(0, 15)] + HEX[randint(0, 15)]
        dlc = randint(3, 8)
        can_id = '00000{0}'.format(id_data)
        payload = [HEX[randint(0, 15)] + HEX[randint(0, 15)] for _ in range(0, dlc)]

        base_timestamp += 0.0001
        attack_data.loc[i, 'Timestamp'] = base_timestamp
        attack_data.loc[i, 'ID'] = can_id
        attack_data.loc[i, 'DLC'] = dlc
        attack_data.loc[i, 'Payload'] = payload
        attack_data.loc[i, 'label'] = 1

    dataset = pandas.concat([dataset, attack_data])

    dataset = dataset.sort_values(by = 'Timestamp')

    return dataset

# def make_fuzzing(dataset: pandas.DataFrame) -> pandas.DataFrame:
#     attack_data = pandas.DataFrame(columns = COLUMNS)
#     base_timestamp = get_base_timestamp(dataset = dataset)
#     end_timestamp = base_timestamp + 1
#
#     i = 0
#     with tqdm() as pbar:
#         while base_timestamp < end_timestamp:
#             pbar.update(1)
#             id_data = HEX[randint(0, 15)] + HEX[randint(0, 15)] + HEX[randint(0, 15)]
#             dlc = randint(3, 8)
#             can_id = '00000{0}'.format(id_data)
#             interval = round(get_interval(can_id = can_id, dataset = dataset), 5)
#             payload = [HEX[randint(0, 15)] + HEX[randint(0, 15)] for _ in range(0, dlc)]
#
#             base_timestamp += interval
#             attack_data.loc[i, 'Timestamp'] = base_timestamp
#             attack_data.loc[i, 'ID'] = can_id
#             attack_data.loc[i, 'DLC'] = str(dlc)
#             attack_data.loc[i, 'Payload'] = ' '.join(payload)
#             attack_data.loc[i, 'label'] = 1
#
#             if base_timestamp is None:
#                 print(base_timestamp)
#                 print(interval)
#                 exit(1)
#
#             i += 1
#
#     dataset = pandas.concat([dataset, attack_data])
#
#     dataset = dataset.sort_values(by = 'Timestamp')
#
#     return dataset


def make_ddos(dataset: pandas.DataFrame) -> pandas.DataFrame:
    attack_data = pandas.DataFrame(columns = COLUMNS)
    base_timestamp = get_base_timestamp(dataset = dataset)

    for i in tqdm(range(0, 4000), leave = True):
        base_timestamp += 0.00025
        attack_data.loc[i, 'Timestamp'] = base_timestamp
        attack_data.loc[i, 'ID'] = '00000000'
        attack_data.loc[i, 'DLC'] = '8'
        attack_data.loc[i, 'Payload'] = '00 00 00 00 00 00 00 00'
        attack_data.loc[i, 'label'] = 1

    dataset = pandas.concat([dataset, attack_data])

    dataset = dataset.sort_values(by = 'Timestamp')

    return dataset


def get_base_timestamp(dataset: pandas.DataFrame) -> float:
    return dataset['Timestamp'].tolist()[random.randint(0, len(dataset) - 1)]


def get_interval(can_id: str, dataset: pandas.DataFrame) -> float:
    total_interval = dataset['Timestamp'].diff().mean()
    data = dataset.loc[dataset['ID'] == can_id]
    if len(data) == 0:
        return total_interval
    else:
        return data['Timestamp'].diff().mean()


def create_can_normal_dataset(input_data: typing.TextIO, target: str) -> None:
    """
    :param input_data: raw data ( CAN )
    :param target: absolute path about dataset
    """

    input_data.readline()
    temp = list()
    for line in tqdm(input_data.readlines(), leave = True):
        if not line == 'Logging stopped.\n':
            line = line.split()
            temp.append(np.array([line[-2], line[1], line[2], ' '.join(line[3:-2])]))
    data = np.array(temp)
    dataframe = pandas.DataFrame(columns = COLUMNS, data = data)
    label = np.array([0 for i in range(len(dataframe))])
    dataframe['label'] = label
    dataframe.to_csv(f'{target}.csv', sep = ',', index = False)

    print(f'File creating is success.')
    print(f'File path is {os.getcwd()}/{target}.csv')
