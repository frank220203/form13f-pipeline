from abc import ABC, abstractmethod
from domain.models.crosswalk import Crosswalk

class CrosswalkRepository(ABC):
    @abstractmethod
    async def add_data(self, crosswalk: Crosswalk) -> Crosswalk:
        pass

    @abstractmethod
    async def get_crosswalk_by_sin(self, sin: str) -> Crosswalk:
        pass