import typing
import os
import pandas


def is_exists() -> bool:
    return True


def make_fuzzing(dataset: pandas.DataFrame) -> pandas.DataFrame:



    return dataset


def make_ddos(dataset: pandas.DataFrame) -> pandas.DataFrame:
    return dataset


def create_can_normal_dataset(input_data: typing.TextIO, target: str) -> None:
    """
    :param input_data: raw data ( CAN )
    :param target: absolute path about dataset
    """
    can_column = ['Timestamp', 'ID', 'DLC', 'Payload']

    dataframe = pandas.read_csv(input_data, sep = '   ', header = None, engine = 'python')
    dataframe = dataframe.drop([1, 3], axis = 1)
    dataframe.columns = can_column
    dataframe['Timestamp'] = dataframe['Timestamp'].str[11:]
    dataframe['ID'] = dataframe['ID'].str[6:]
    dataframe['DLC'] = dataframe['DLC'].str[6:]
    dataframe['Payload'] = dataframe['Payload'].str[1:]

    dataframe.to_csv(f'{target}.csv', sep = ',', index = False)

    print(f'File creating is success.')
    print(f'File path is {os.getcwd()}/{target}.csv')
