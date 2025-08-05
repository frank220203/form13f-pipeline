from abc import ABC, abstractmethod
from typing import List

class PaserService(ABC):
    @abstractmethod
    def find_documents_urls(self, data: str) -> List[str]:
        pass

    @abstractmethod
    def find_portfolio_urls(self, data: str) -> dict:
        pass

    @abstractmethod
    def find_portfolio_issuers(self, data: str) -> List[dict]:
        pass