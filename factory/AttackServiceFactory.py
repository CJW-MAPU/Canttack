from service.CanAttackService import CanAttackService
from service.FDAttackService import FDAttackService

from common.Type import DataType


class AttackServiceFactory:
    __can_service = CanAttackService()
    __fd_service = FDAttackService()

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_service(cls, data_type):
        if data_type == DataType.CAN.value:
            service = cls.__can_service
        elif data_type == DataType.FD.value:
            service = cls.__fd_service
        else:
            service = None

        return service