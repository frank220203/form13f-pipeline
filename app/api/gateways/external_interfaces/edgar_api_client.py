from abc import ABC, abstractmethod

class EdgarApiClient(ABC):
    @abstractmethod
    def get_fillings_list(self, url: str, headers: dict, params: dict):
        pass