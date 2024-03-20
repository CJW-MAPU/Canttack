from abc import *


class DatasetService(metaclass = ABCMeta):
    @abstractmethod
    def make_can_data(self, file):
        pass

    @abstractmethod
    def make_fd_data(self, file):
        pass
