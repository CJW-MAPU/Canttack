from service.AvanteDatasetService import AvanteDatasetService
from service.CarnivalDatasetService import CarnivalDatasetService

from common.Type import VehicleType
from exception import ExceptionController


class DatasetServiceFactory:
    __avante_service = AvanteDatasetService()
    __carnival_service = CarnivalDatasetService()

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_service(cls, vehicle_type: VehicleType):
        if vehicle_type == VehicleType.AVANTE.value:
            service = cls.__avante_service
        elif vehicle_type == VehicleType.CARNIVAL.value:
            service = cls.__carnival_service
        else:
            raise ExceptionController.CallNotSupportVehicleTypeException()

        return service
