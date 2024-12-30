from abc import ABC, abstractmethod

class EdgarApiService(ABC):
    @abstractmethod
    def get_fillings_list(self, url: str, headers: dict, params: dict) -> str:
        pass