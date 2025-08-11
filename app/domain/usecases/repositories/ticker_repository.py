from abc import ABC, abstractmethod
from typing import List
from domain.models.ticker import Ticker

class TickerRepository(ABC):
    @abstractmethod
    async def add_data(self, ticker: Ticker) -> Ticker:
        pass

    @abstractmethod
    async def get_all_tickers(self) -> List[Ticker]:
        pass