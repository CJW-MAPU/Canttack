from exception.TypeMatchException import TypeMatchException


def CallTypeMatchException():
    raise TypeMatchException('Do not match between dataset type and attack type.\n'
                             'If need you help, please read help.')
