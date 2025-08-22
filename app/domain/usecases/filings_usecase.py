import json
from typing import List

from domain.models.submission import Submission

from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.edgar_service import EdgarService
from domain.usecases.services.message_handler import MessageHandler
from domain.usecases.services.xml_parser_service import XmlPaserService
from domain.usecases.services.html_parser_service import HtmlPaserService

# cik : sec에 등록된 기업 고유 식별번호
# filings : 제출물
# documents : 일반 문서
# portfolio : 바구니
# issuer : 상장회사
class FilingsUsecase:

    __api_caller: ApiCaller
    __edgar_service: EdgarService
    __message_handler: MessageHandler
    __xml_paser_service: XmlPaserService
    __html_paser_servcie: HtmlPaserService
    
    def __init__(
            self, 
            api_caller: ApiCaller, 
            edgar_service: EdgarService, 
            message_handler: MessageHandler,
            xml_paser_service: XmlPaserService,
            html_paser_service: HtmlPaserService
    ):
        self.__api_caller = api_caller
        self.__edgar_service = edgar_service
        self.__message_handler = message_handler
        self.__xml_paser_service = xml_paser_service
        self.__html_paser_servcie = html_paser_service
    
    
    async def get_all_tickers(self, headers: dict) -> dict:
        url = self.__edgar_service.get_edgar_tickers_url()
        tickers = await self.__api_caller.call(url=url, headers=headers)

        # Kafak msg 발행
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

        # Kafak msg 발행
        await self.__message_handler.publish('submission', submissions)
        return submissions
    
    async def get_portfolio(
            self,
            cik: str,
            headers: dict,
            accession_number: str
    ) -> dict:
        portfolio = {}
        # Meta 추출
        meta_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number, type="meta")
        response = await self.__api_caller.call(url=meta_url, headers=headers)
        portfolio.update(self.__xml_paser_service.xml_to_dict(response))

        # File list 추출
        data_list_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number)
        response = await self.__api_caller.call(url=data_list_url, headers=headers)

        # Data 추출
        xml_link = self.__html_paser_servcie.find_xml(response)
        issuers_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number, type="data", file_name=xml_link)
        response = await self.__api_caller.call(url=issuers_url, headers=headers)
        portfolio.update(self.__xml_paser_service.xml_to_dict(response))

        # Kafak msg 발행
        await self.__message_handler.publish('portfolio', portfolio)
        return portfolio