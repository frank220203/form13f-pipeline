from abc import ABC, abstractmethod

class ApiCaller(ABC):
    @abstractmethod
    async def call(self, url: str, headers: dict, params: dict) -> str:
        pass
    @abstractmethod
    async def call_for_file(self, url: str, headers: dict, params: dict) -> bytes:
        pass