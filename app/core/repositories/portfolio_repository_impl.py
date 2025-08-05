from motor.motor_asyncio import AsyncIOMotorClient
from core.entities.portfolio_documents import PortfolioDocument

from domain.models.portfolio import Portfolio
from domain.usecases.repositories.portfolio_repository import PortfolioRepository

class PortfolioRepositoryImpl(PortfolioRepository):

    async def init_db(self, url: str) -> None:
        client = AsyncIOMotorClient(url)
        await self.__beanie_repository.init_beanie(database=client.portfolio, document_models=[Portfolio])

    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        portfolio_doc = PortfolioDocument(**portfolio.model_dump())
        await portfolio_doc.insert()
        return Portfolio(**portfolio_doc.model_dump())
    
    async def get_portfolio_by_date(self, date: str) -> Portfolio:
        portfolio_doc = await PortfolioDocument.find_one(PortfolioDocument.report_period == date)
        if portfolio_doc:
            return Portfolio(**portfolio_doc.model_dump())
        return None
    
    async def get_all_portfolios(self):
        return await super().get_all_portfolios()