import ast
import json
from typing import List

from domain.models.ticker import Ticker
from domain.models.crosswalk import Crosswalk
from domain.models.portfolios.portfolio import Portfolio
from domain.models.submissions.submission import Submission

from domain.usecases.services.prompt_service import PromptService

from domain.usecases.repositories.ticker_repository import TickerRepository
from domain.usecases.repositories.portfolio_repository import PortfolioRepository
from domain.usecases.repositories.crosswalk_repository import CrosswalkRepository
from domain.usecases.repositories.submission_repository import SubmissionRepository

class PipelineUsecase:

    __prompt_service: PromptService
    __ticker_repository: TickerRepository
    __portfolio_repository: PortfolioRepository
    __crosswalk_repository: CrosswalkRepository
    __submission_repository: SubmissionRepository

    def __init__(
            self, 
            prompt_service: PromptService,
            ticker_repository: TickerRepository, 
            portfolio_repository: PortfolioRepository, 
            crosswalk_repository: CrosswalkRepository, 
            submission_repository: SubmissionRepository
            ):
        self.__prompt_service = prompt_service
        self.__ticker_repository = ticker_repository
        self.__portfolio_repository = portfolio_repository
        self.__crosswalk_repository = crosswalk_repository
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
        
        portfolio = await self.__portfolio_repository.add_data(Portfolio(**data))
        sins = []
        dup_cusip = set()
        for issuer in portfolio.issuers:
            if issuer.cusip not in dup_cusip:
                sins.append({'sin':issuer.cusip, 'name':issuer.name_of_issuer})
                dup_cusip.add(issuer.cusip)
        msg = {'data':sins, 'type':'cusip'}
        return msg
    
    async def load_crosswalks(self, data: str) -> List[dict]:

        try:
            while isinstance(data, str):
                data = json.loads(data)
        except Exception as e:
            raise e     
        
        request_sins = []
        for sin in data['data']:
            if not await self.__crosswalk_repository.get_crosswalk_by_sin(Crosswalk(sin=sin['sin'], name=sin['name'])) :
                request_sins.append(sin)
        answer = "[]"
        if request_sins:
            if data['type'] == "cusip":
                answer = await self.__prompt_service.get_naics(request_sins, data['type'])

        try:
            naics_list = ast.literal_eval(answer)
        except Exception as e:
            raise e  
        
        for naics in naics_list:
            await self.__crosswalk_repository.add_data(Crosswalk(sin=naics['cusip'], naics=naics['naics'], industry=naics['industry']))
        return naics_list