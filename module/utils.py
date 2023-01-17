import typing
import os
import pandas
import numpy as np
import random
import json

from tqdm import tqdm

CAN_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload']
FD_COLUMNS = ['Timestamp', 'ID', 'DLC', 'Flg', 'Dir', 'Payload']
HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


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


def get_base_timestamp(dataset: pandas.DataFrame) -> float:
    """
    :param dataset: normal dataset ( .csv )
    :return: the timestamp at which the attack will be injected
    """
    return dataset['Timestamp'].tolist()[random.randint(0, len(dataset) - 1)]


def get_interval(identifier: str, dataset: pandas.DataFrame) -> float:
    """
    :param identifier: ID for which you want to get the average time interval
    :param dataset: normal dataset ( .csv )
    :return:
    """
    total_interval = dataset['Timestamp'].diff().mean()
    data = dataset.loc[dataset['ID'] == identifier]
    if len(data) == 0:
        return total_interval
    else:
        return data['Timestamp'].diff().mean()


def create_can_normal_dataset(input_data: typing.TextIO, target: str) -> None:
    """
    :param input_data: raw data ( CAN.txt )
    :param target: absolute path about dataset
    """

    input_data.readline()
    temp = list()
    for line in tqdm(input_data.readlines(), leave = True):
        if not line == 'Logging stopped.\n':
            line = line.split()
            temp.append(np.array([line[-2], line[1], line[2], ' '.join(line[3:-2])]))
    data = np.array(temp)
    dataframe = pandas.DataFrame(columns = CAN_COLUMNS, data = data)
    label = np.array([0 for i in range(len(dataframe))])
    dataframe['label'] = label
    dataframe.to_csv(f'{target}.csv', sep = ',', index = False)

    print(f'File creating is success.')
    print(f'File path is {os.getcwd()}/{target}.csv')


def create_can_fd_normal_dataset(input_data: typing.TextIO, target: str) -> None:
    """
    :param input_data: raw data ( CAN-FD.txt )
    :param target: absolute path about dataset
    """

    input_data.readline()
    data = list()
    temp = None
    string = None
    dlc = 0

    for line in tqdm(input_data.readlines(), leave = True):
        if not line == 'Logging stopped.\n':
            line = line.split()
            if len(line) == 14:
                temp = [line[-2], line[1], line[3], line[2], line[-1]]
                string = ' '.join(line[4:-2])
                dlc = (int(line[3], 16) // 8) - 1
            else:
                string = f'{string} {" ".join(line)}'
                dlc -= 1

            if dlc == 0:
                temp.append(string)
                data.append(np.array(temp))

    data = np.array(data)
    dataframe = pandas.DataFrame(columns = FD_COLUMNS, data = data)
    label = np.array([0 for i in range(len(dataframe))])
    dataframe['label'] = label
    dataframe.to_csv(f'{target}.csv', sep = ',', index = False)

    print(f'File creating success.')
    print(f'File path is {os.getcwd()}/{target}.csv')


def json_parser(filepath: str, data_type: str, attack_type: str) -> dict:
    with open(filepath, 'r') as file:
        jsonfile = json.load(file)

    return jsonfile[data_type][attack_type]
