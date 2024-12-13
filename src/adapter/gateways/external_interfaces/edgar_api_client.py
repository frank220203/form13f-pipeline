from abc import ABC, abstractmethod

class EdgarApiClient(ABC):
    @abstractmethod
    def get_13f_data(cik: str, start: int, count: int):
        pass