from abc import ABC, abstractmethod

class LoggerManager(ABC):
    @abstractmethod
    def get_logger() :
        pass