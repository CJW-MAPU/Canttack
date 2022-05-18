import pandas as pd
from pandas import read_csv
from module.DatasetFactory import DatasetFactory

if __name__ == '__main__':
    f = open('data/normal_run_data.txt')

    dataset_factory = DatasetFactory(f)
    print(dataset_factory.fuzzing_builder().add_attack().build())
