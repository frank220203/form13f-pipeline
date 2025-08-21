from abc import ABC, abstractmethod

class ApiCaller(ABC):
    @abstractmethod
    async def call(self, url: str, headers: dict, params: dict) -> str:
        pass