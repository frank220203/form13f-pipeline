from typing import List, Optional
from domain.models.portfolios.portfolio import Portfolio
from domain.usecases.repositories.portfolio_repository import PortfolioRepository

class PortfolioService():
    
    __portfolioRepository: PortfolioRepository

    def __init__(self, portfolio_repository: PortfolioRepository):
        self.__portfolioRepository = portfolio_repository

    async def add_data(self, portfolio: Portfolio) -> Portfolio:
        # 포트폴리오의 날짜 데이터 뽑아서 중복체크 필요
        return await self.__portfolioRepository.add_data(portfolio)
    
    async def get_portfolio(self, date: str) -> Optional[Portfolio]:
        return await self.__portfolioRepository.get_portfolio_by_date(date)
    
    async def get_all_portfolios(self) -> List[Portfolio]:
        return await self.__portfolioRepository.get_all_portfolio()