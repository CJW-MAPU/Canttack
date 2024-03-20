from exception.NotSupportAttackServiceException import NotSupportAttackServiceException
from exception.NotSupportAttackTypeException import NotSupportAttackTypeException
from exception.NotSupportDataTypeException import NotSupportDataTypeException
from exception.InvalidJSONFileException import InvalidJSONFileException
from exception.NotSupportVehicleTypeException import NotSupportVehicleTypeException
from exception.NotSupportDatasetServiceException import NotSupportDatasetServiceException


def CallNotSupportAttackServiceException(data_type: str, attack_type: str):
    raise NotSupportAttackServiceException(f'The entered service [ {data_type} : {attack_type} ] is an unsupported service.'
                                     f'\n If need you help, please read help.')


def CallNotSupportDatasetServiceException(vehicle_type: str, data_type: str):
    raise NotSupportDatasetServiceException(f'The entered service [ {vehicle_type} : {data_type} ] is an unsupported service.'
                                            f'\n If need you help, please read help.')


def CallNotSupportAttackTypeException():
    raise NotSupportAttackTypeException('The entered attack type is an unsupported type.\n'
                                        'If need you help, please read help.')


def CallNotSupportDataTypeException():
    raise NotSupportDataTypeException('The entered data type is an unsupported type.\n'
                                      'If need you help, please read help.')


def CallInvalidJSONFileException():
    raise InvalidJSONFileException('The format of the input JSON file is not valid.\n'
                                   'Please check the format of the file.')


def CallNotSupportVehicleTypeException():
    raise NotSupportVehicleTypeException('The entered vehicle type is an unsupported type.\n'
                                         'If need you help, please read help.')
