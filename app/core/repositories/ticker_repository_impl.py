from core.entities.portfolio_document import PortfolioDocument

from domain.models.ticker import Ticker
from domain.usecases.repositories.ticker_repository import TickerRepository

class TickerRepositoryImpl(TickerRepository):

    async def add_data(self, ticker: Ticker) -> Ticker:
        ticker_doc = PortfolioDocument(**ticker.model_dump())
        await ticker_doc.insert()
        return Ticker(**ticker_doc.model_dump())