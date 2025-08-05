from abc import ABC, abstractmethod
from typing import List

class EdgarService(ABC):
    @abstractmethod
    def get_edgar_url(self) -> dict:
        pass
    @abstractmethod
    async def get_all_filings(self, cik: str, filing_type: str) -> List:
        pass