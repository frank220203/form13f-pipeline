from typing import List
from core.entities.ticker_document import TickerDocument

from domain.models.ticker import Ticker
from domain.usecases.repositories.ticker_repository import TickerRepository

class TickerRepositoryImpl(TickerRepository):

    async def add_data(self, ticker: Ticker) -> Ticker:
        ticker_doc = TickerDocument(**ticker.model_dump())
        await ticker_doc.insert()
        return Ticker(**ticker_doc.model_dump())
    
    async def get_all_tickers(self) -> List[Ticker]:
        pass