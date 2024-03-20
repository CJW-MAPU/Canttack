import typing
import numpy as np
import pandas
from tqdm import tqdm

from service.DatasetService import DatasetService


class AvanteDatasetService(DatasetService):
    COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_can_data(cls, file: typing.TextIO) -> pandas.DataFrame:
        file.readline()
        temp = list()

        for line in tqdm(file.readlines(), leave = True):
            if not line == 'Logging stopped.\n':
                line = line.split()
                temp.append(np.array([line[-2], line[1], line[2], ' '.join(line[3:-2])]))
        data = np.array(temp)
        dataframe = pandas.DataFrame(columns = cls.COLUMNS, data = data)
        label = np.array([0 for i in range(len(dataframe))])
        dataframe['label'] = label

        return dataframe

    @classmethod
    def make_fd_data(cls, file) -> pandas.DataFrame:
        file.readline()
        data = list()
        temp = None
        string = None
        dlc = 0

        for line in tqdm(file.readlines(), leave = True):
            if not line == 'Logging stopped.\n':
                line = line.split()
                if len(line) == 14:
                    temp = [line[-2], line[1], line[3]]
                    string = ' '.join(line[4:-2])
                    dlc = (int(line[3], 16) // 8) - 1
                else:
                    string = f'{string} {" ".join(line)}'
                    dlc -= 1

                if dlc == 0:
                    temp.append(string)
                    data.append(np.array(temp))

        data = np.array(data)
        dataframe = pandas.DataFrame(columns = cls.COLUMNS, data = data)
        label = np.array([0 for i in range(len(dataframe))])
        dataframe['label'] = label

        return dataframe
