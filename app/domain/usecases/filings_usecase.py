import json
from typing import List

from domain.models.submission import Submission

from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.edgar_service import EdgarService
from domain.usecases.services.parser_service import PaserService
from domain.usecases.services.message_handler import MessageHandler

# cik : sec에 등록된 기업 고유 식별번호
# filings : 제출물
# documents : 일반 문서
# portfolio : 바구니
# issuer : 상장회사
class FilingsUsecase:

    __api_caller: ApiCaller
    __edgar_service: EdgarService
    __paser_service: PaserService
    __message_handler: MessageHandler
    
    def __init__(
            self, 
            api_caller: ApiCaller, 
            edgar_service: EdgarService, 
            paser_service: PaserService, 
            message_handler: MessageHandler
    ):
        self.__api_caller = api_caller
        self.__edgar_service = edgar_service
        self.__paser_service = paser_service
        self.__message_handler = message_handler
    
    
    async def get_all_tickers(self, headers: dict) -> dict:
        url = self.__edgar_service.get_edgar_tickers_url()
        tickers = await self.__api_caller.call(url=url, headers=headers)
        await self.__message_handler.publish('ticker', tickers)
        return tickers
    
    async def get_all_submissions(
            self,
            cik: str,
            headers: dict,
            filing_type: List[str] = None,
    ) -> dict:
        url = self.__edgar_service.get_submissions_url(cik)
        response = await self.__api_caller.call(url=url, headers=headers)
        submissions = response
        if filing_type:
            filtered_submissions = self.__edgar_service.find_submissions(Submission(**json.loads(response)), filing_type)
            submissions = filtered_submissions.model_dump()
        await self.__message_handler.publish('submission', submissions)
        return submissions
    
    async def get_portfolio(
            self,
            cik: str,
            headers: dict,
            accession_number: str
    ) -> dict:
        portfolio = {}
        for url in self.__edgar_service.get_portfolio_url(cik, accession_number):
            response = await self.__api_caller.call(url=url, headers=headers)
            portfolio.update(self.__paser_service.xml_to_dict(response))
        await self.__message_handler.publish('portfolio', portfolio)
        return portfolio