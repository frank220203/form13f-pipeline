from abc import ABC, abstractmethod
from typing import List
from domain.models.portfolios.portfolio import Portfolio

class PortfolioRepository(ABC):
    @abstractmethod
    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        pass

    @abstractmethod
    async def get_portfolio_by_cik(self, cik: str) -> Portfolio:
        pass

    @abstractmethod
    async def get_distinct_issuers(self, portfolio: Portfolio) -> List:
        pass

    @abstractmethod
    async def get_all_portfolios(self) -> List[Portfolio]:
        pass