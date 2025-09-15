from typing import List
from pymongo.errors import DuplicateKeyError
from core.entities.portfolio_document import PortfolioDocument

from domain.models.portfolios.portfolio import Portfolio
from domain.usecases.repositories.portfolio_repository import PortfolioRepository

class PortfolioRepositoryImpl(PortfolioRepository):
    
    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        portfolio_doc = PortfolioDocument(**portfolio.model_dump())
        try:
            await portfolio_doc.insert()
        except DuplicateKeyError:
            print("portfolio_doc 중복")
        return Portfolio(**portfolio_doc.model_dump())
    
    async def get_portfolio_by_cik(self, cik: str) -> Portfolio:
        portfolio_doc = await PortfolioDocument.find_one({'header_data.filerInfo.filer.credentials.cik' : cik})
        return Portfolio(**portfolio_doc.model_dump())
    
    async def get_distinct_issuers(self, portfolio: Portfolio) -> List:
        portfolio_doc = PortfolioDocument(**portfolio.model_dump())
        pipeline = [
            {
                '$unwind' : {
                    'path' : '$issuers'
                }
            },
            {
                '$group' : {
                    '_id' : '$issuers.cusip',
                    'name' : {
                        '$first' : '$issuers.name_of_issue'
                    }
                }
            }
        ]
        return await portfolio_doc.find().aggregate(pipeline).to_list
    
    async def get_all_portfolios(self):
        return await super().get_all_portfolios()