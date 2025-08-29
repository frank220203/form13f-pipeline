import json
from typing import List

from domain.models.ticker import Ticker
from domain.models.portfolios.portfolio import Portfolio
from domain.models.submissions.submission import Submission

from domain.usecases.repositories.ticker_repository import TickerRepository
from domain.usecases.repositories.portfolio_repository import PortfolioRepository
from domain.usecases.repositories.submission_repository import SubmissionRepository

class PipelineUsecase:

    __ticker_repository: TickerRepository
    __portfolio_repository: PortfolioRepository
    __submission_repository: SubmissionRepository

    def __init__(self, ticker_repository: TickerRepository, portfolio_repository: PortfolioRepository, submission_repository: SubmissionRepository):
        self.__ticker_repository = ticker_repository
        self.__portfolio_repository = portfolio_repository
        self.__submission_repository = submission_repository

    async def load_tickers(self, data: str) -> List[dict]:
        
        try:
            while isinstance(data, str):
                data = json.loads(data)
        except Exception as e:
            raise e     
        fields = data['fields']
        tickers = data['data']
        ticker_list = []
        for ticker in tickers:
            ticker_dict = dict(zip(fields, ticker))
            ticker_list.append(await self.__ticker_repository.add_data(Ticker(**ticker_dict)))

        return ticker_list
    
    async def load_submissions(self, data: str) -> dict:
        
        try:
            while isinstance(data, str):
                data = json.loads(data)
        except Exception as e:
            raise e     
        
        return await self.__submission_repository.add_data(Submission(**data))
    
    async def load_portfolios(self, data: str) -> dict:

        try:
            while isinstance(data, str):
                data = json.loads(data)
        except Exception as e:
            raise e     
        
        return await self.__portfolio_repository.add_data(Portfolio(**data))
    
    async def get_issuers_cik(self, cik: str) -> List[str]:
        portfolio = PortfolioRepository.get_portfolio_by_cik(cik)