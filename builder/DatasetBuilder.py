import pandas
import typing
import os

from factory.DatasetServiceFactory import DatasetServiceFactory
from service.DatasetService import DatasetService
from common.Type import DataType
from exception import ExceptionController


class DatasetBuilder:
    __data_type: str = None
    __file: typing.TextIO = None
    __dataset: pandas.DataFrame = None
    __dest: str = None
    __dataset_service_factory: DatasetServiceFactory = DatasetServiceFactory()
    __dataset_service: DatasetService = None

    @classmethod
    def __init__(cls, file: typing.TextIO, dest: str, vehicle_type):
        cls.__file = file
        cls.__dataset_service = cls.__dataset_service_factory.create_service(vehicle_type = vehicle_type)
        cls.__dest = dest

    @classmethod
    def set_data_type(cls, data_type: str):
        cls.__data_type = data_type

    @classmethod
    def create_dataset(cls):
        if cls.__data_type == DataType.CAN.value:
            cls.__dataset = cls.__dataset_service.make_can_data(file = cls.__file)
        elif cls.__data_type == DataType.FD.value:
            cls.__dataset = cls.__dataset_service.make_fd_data(file = cls.__file)
        else:
            raise ExceptionController.CallNotSupportDataTypeException()

    @classmethod
    def build(cls) -> None:
        cls.__dataset.to_csv(f'data/{cls.__dest}.csv', sep = ',', index = False)
        print()
        print(f'File creating is success.')
        print(f'File path is {os.getcwd()}/data/{cls.__dest}.csv')
