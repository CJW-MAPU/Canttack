def print_directory_is_not_exists(path: str) -> None:
    print('Directory Not Found.')
    print('Creating Directory. ' + path)
    print()
    print()


def print_normal_dataset_is_not_exists(path: str) -> None:
    print("you don't have normal dataset.")
    print('Creating Dataset. ' + path)
    print()
    print()


def print_normal_dataset_is_exists(path: str) -> None:
    print('you already have normal dataset.')
    print('Dataset path is ' + path)
    print('If you want get normal run dataset then please call pandas.read_csv() method.')
    print()
    print()
