from abc import ABC, abstractmethod


class AbstractService(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        pass


