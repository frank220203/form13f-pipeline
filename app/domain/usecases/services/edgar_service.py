from abc import ABC, abstractmethod
from typing import List
from domain.models.submissions.filings.recent import Recent

class EdgarService(ABC):
    @abstractmethod
    def get_edgar_tickers_url(self) -> dict:
        pass
    @abstractmethod
    def get_submissions_url(self, cik: str, filing_type: str) -> List:
        pass
    @abstractmethod
    def get_portfolio_url(self, cik: str, accession_number: str, type: str, file_name: str) -> str:
        pass
    @abstractmethod
    def filter_recent(self, recent: Recent, filings_type: List[str]) -> Recent:
        pass