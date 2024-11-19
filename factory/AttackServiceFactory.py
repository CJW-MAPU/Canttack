from service.CanAttackService import CanAttackService
from service.FDAttackService import FDAttackService
from service.AttackService import AttackService

from common.Type import DataType

from exception import ExceptionController


class AttackServiceFactory:
    __can_service = CanAttackService()
    __fd_service = FDAttackService()

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_service(cls, data_type: str) -> AttackService:
        if data_type == DataType.CAN.value:
            service = cls.__can_service
        elif data_type == DataType.FD.value:
            service = cls.__fd_service
        else:
            service = ExceptionController.CallNotSupportDataTypeException()

        return service
