from abc import ABC, abstractmethod
from typing import List

class PromptService(ABC):
    @abstractmethod
    async def get_response(self, request: str) -> str:
        pass

    @abstractmethod
    async def get_naics(self, sins: List[str], type: str) -> str:
        pass