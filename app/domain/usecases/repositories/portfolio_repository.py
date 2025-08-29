from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.portfolios.portfolio import Portfolio

class PortfolioRepository(ABC):
    @abstractmethod
    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        pass

    @abstractmethod
    async def get_portfolio_by_date(self, date: str) -> Optional[Portfolio]:
        pass

    @abstractmethod
    async def get_all_portfolios(self) -> List[Portfolio]:
        pass