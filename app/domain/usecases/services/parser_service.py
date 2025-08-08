from abc import ABC, abstractmethod
from typing import List

class PaserService(ABC):
    @abstractmethod
    def xml_to_dict(self, data: str) -> dict:
        pass