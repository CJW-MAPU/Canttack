from exception.NotSupportServiceException import NotSupportServiceException
from exception.NotSupportAttackTypeException import NotSupportAttackTypeException
from exception.NotSupportDataTypeException import NotSupportDataTypeException
from exception.InvalidJSONFileException import InvalidJSONFileException


def CallNotSupportServiceException(data_type: str, attack_type: str):
    raise NotSupportServiceException(f'The entered service [ {data_type} : {attack_type} ] is an unsupported service.'
                                     f'\n If need you help, please read help.')


def CallNotSupportAttackTypeException():
    raise NotSupportAttackTypeException('The entered attack type is an unsupported type.\n'
                                        'If need you help, please read help.')


def CallNotSupportDataTypeException():
    raise NotSupportDataTypeException('The entered data type is an unsupported type.\n'
                                      'If need you help, please read help.')


def CallInvalidJSONFileException():
    raise InvalidJSONFileException('The format of the input JSON file is not valid.\n'
                                   'Please check the format of the file')
