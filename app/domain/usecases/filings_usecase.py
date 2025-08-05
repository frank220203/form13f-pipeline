from typing import List

from domain.models.issuer import Issuer
from domain.models.portfolio import Portfolio

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
    
    def __init__(self, api_caller: ApiCaller, edgar_service: EdgarService, paser_service: PaserService, message_handler: MessageHandler):
        self.__api_caller = api_caller
        self.__edgar_service = edgar_service
        self.__paser_service = paser_service
        self.__message_handler = message_handler
    
    
    async def get_all_tickers(self, endpoint:str, headers: dict) -> dict:
        url = self.__edgar_service.get_edgar_url() + endpoint
        return await self.__api_caller.call(url=url, headers=headers)

    async def get_documents_urls(
            self,
            endpoint: str, 
            headers: dict,
            params: dict
    ) -> List[str]:
        data = await self.__edgar_service.call(endpoint, headers, params)
        urls = self.__paser_service.find_documents_urls(data)
        return urls
        
    async def get_portfolio_urls(
            self,
            endpoint: str,
            headers: dict
    ) -> dict:
        data = await self.__edgar_service.call(endpoint, headers)
        portfolio_urls = self.__paser_service.find_portfolio_urls(data)
        return portfolio_urls
    
    async def get_portfolio(
            self,
            endpoint: str,
            headers: dict,
            meta: dict
    ) -> Portfolio:
        data = await self.__edgar_service.call(endpoint, headers)
        issuers_dict = self.__paser_service.find_portfolio_issuers(data)
        issuers = []
        for issuer in issuers_dict:
            issuers.append(Issuer.model_validate(issuer))
        portfolio = Portfolio(cik=meta['cik'], filing_accepted=meta['Accepted'], report_period=meta['Period of Report'], create_at=meta['Effectiveness Date'], issuers=issuers)
        await self.__message_handler.publish("portfolio", portfolio)
        return portfolio