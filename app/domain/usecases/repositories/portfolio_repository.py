from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.portfolio import Portfolio

class PortfolioRepository(ABC):
    @abstractmethod
    async def init_db(self, url: str) -> None:
        pass

    @abstractmethod
    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        pass

    @abstractmethod
    async def get_portfolio_by_date(self, date: str) -> Optional[Portfolio]:
        pass

    @abstractmethod
    async def get_all_portfolios(self) -> List[Portfolio]:
        pass