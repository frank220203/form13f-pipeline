from abc import ABC, abstractmethod

class ApiCaller(ABC):
    @abstractmethod
    def call(self, url: str, headers: dict, params: dict) -> str:
        pass