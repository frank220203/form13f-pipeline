import json
from typing import List

from domain.models.ticker import Ticker
from domain.models.issuer import Issuer
from domain.models.portfolio import Portfolio
from domain.models.submission import Submission

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
        
        portfolio_dict = {}
        portfolio_dict.update(header_data=data['edgarSubmission']['headerData'], form_data=data['edgarSubmission']['formData'])
        issuers = []
        for issuer in data['informationTable']['infoTable'] :
            issuers.append(Issuer(**issuer))
        portfolio_dict.update({'issuers':issuers})
        
        return await self.__portfolio_repository.add_data(Portfolio(**portfolio_dict))