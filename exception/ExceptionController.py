from exception.TypeMatchException import TypeMatchException
from exception.NotSupportAttackTypeException import NotSupportAttackTypeException
from exception.NotSupportDataTypeException import NotSupportDataTypeException
from exception.InvalidJSONFileException import InvalidJSONFileException


def CallTypeMatchException():
    raise TypeMatchException('Do not match between dataset type and attack type.\n'
                             'If need you help, please read help.')


def CallNotSupportAttackTypeException():
    raise NotSupportAttackTypeException('The entered attack type is an unsupported type.\n'
                                        'If need you help, please read help.')


def CallNotSupportDataTypeException():
    raise NotSupportDataTypeException('The entered data type is an unsupported type.\n'
                                      'If need you help, please read help.')


def CallInvalidJSONFileException():
    raise InvalidJSONFileException('The format of the input JSON file is not valid.\n'
                                   'Please check the format of the file')
