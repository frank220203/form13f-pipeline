from abc import ABC, abstractmethod

class DbManager(ABC):
    @abstractmethod
    def init_db(self) :
        pass