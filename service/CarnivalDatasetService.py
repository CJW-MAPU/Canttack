import typing
import pandas
import numpy as np
from tqdm import tqdm

from service.DatasetService import DatasetService
from exception import ExceptionController
from common.Type import VehicleType, DataType


class CarnivalDatasetService(DatasetService):
    __COLUMNS = ['Timestamp', 'ID', 'DLC', 'Payload']

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def make_can_data(cls, file):
        raise ExceptionController.CallNotSupportDatasetServiceException(vehicle_type = VehicleType.CARNIVAL.value,
                                                                        data_type = DataType.CAN.value)

    @classmethod
    def make_fd_data(cls, file: typing.TextIO) -> pandas.DataFrame:
        for i in range(4):
            file.readline()
        data = list()
        temp = None
        string = None

        for line in tqdm(file.readlines(), leave = True):
            line = line.split()
            temp = [line[3], f'00000{line[1][:3]}', format(int(line[2]), 'x')]
            string = ' '.join(line[4:])
            temp.append(string)
            data.append(np.array(temp))

        data = np.array(data)
        dataframe = pandas.DataFrame(columns = cls.__COLUMNS, data = data)
        label = np.array([0 for i in range(len(dataframe))])
        dataframe['label'] = label

        return dataframe
