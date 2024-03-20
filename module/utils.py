import pandas
import random
import json


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


def json_parser(filepath: str, data_type: str, attack_type: str) -> dict:
    with open(filepath, 'r') as file:
        jsonfile = json.load(file)

    return jsonfile[data_type][attack_type]
