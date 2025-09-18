import json
from typing import List
from datetime import date

from domain.models.portfolios.portfolio import Portfolio
from domain.models.submissions.submission import Submission

from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.dart_service import DartService
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
    __dart_service: DartService
    __edgar_service: EdgarService
    __message_handler: MessageHandler
    __xml_paser_service: XmlPaserService
    __html_paser_servcie: HtmlPaserService
    
    def __init__(
            self, 
            api_caller: ApiCaller, 
            dart_service: DartService,
            edgar_service: EdgarService, 
            message_handler: MessageHandler,
            xml_paser_service: XmlPaserService,
            html_paser_service: HtmlPaserService
    ):
        self.__api_caller = api_caller
        self.__edgar_service = edgar_service
        self.__dart_service = dart_service
        self.__message_handler = message_handler
        self.__xml_paser_service = xml_paser_service
        self.__html_paser_servcie = html_paser_service
    
    
    async def get_all_tickers(self, headers: dict) -> dict:
        url = self.__edgar_service.get_edgar_tickers_url()
        tickers = await self.__api_caller.call(url=url, headers=headers)

        # Kafka msg 발행
        await self.__message_handler.publish("ticker", tickers)
        return tickers
    
    async def get_all_submissions(
            self,
            cik: str,
            headers: dict,
            filing_type: List[str] = None,
    ) -> dict:
        url = self.__edgar_service.get_submissions_url(cik)
        response = await self.__api_caller.call(url=url, headers=headers)
        submissions = Submission(**json.loads(response))
        if filing_type:
            filtered_recent = self.__edgar_service.filter_recent(submissions.filings.recent, filing_type)
            submissions.filings.recent = filtered_recent

        # Kafka msg 발행
        await self.__message_handler.publish("submission", submissions.model_dump())
        return submissions.model_dump()
    
    async def get_portfolio(
            self,
            cik: str,
            headers: dict,
            accession_number: str
    ) -> dict:
        # Meta 추출
        meta_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number, type="meta")
        response = await self.__api_caller.call(url=meta_url, headers=headers)
        header_data = self.__xml_paser_service.xml_to_dict(response)['edgarSubmission']['headerData']
        form_data = self.__xml_paser_service.xml_to_dict(response)['edgarSubmission']['formData']

        # Filing list 추출
        data_list_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number)
        response = await self.__api_caller.call(url=data_list_url, headers=headers)

        # Data 추출
        xml_link = self.__html_paser_servcie.find_xml(response)
        issuers_url = self.__edgar_service.get_portfolio_url(cik=cik, accession_number=accession_number, type="data", file_name=xml_link)
        response = await self.__api_caller.call(url=issuers_url, headers=headers)
        info_table = self.__xml_paser_service.xml_to_dict(response)['informationTable']['infoTable']
        portfolio = Portfolio(header_data=header_data, form_data=form_data, issuers=info_table)

        # Kafka msg 발행
        await self.__message_handler.publish("portfolio", portfolio.model_dump())
        return portfolio.model_dump()
    
    async def get_corp_code(self) -> str:
        corp_code_url = self.__dart_service.get_corp_code_url()
        response = await self.__api_caller.call_for_file(url=corp_code_url, headers={})
        file_name = f"corp_code_{date.today().strftime('%Y%m%d')}.zip".encode("utf-8")
        try:
            response = await self.__message_handler.publish_files("corp_code", file_name, response)
        except Exception as e:
            print(f"에러 : {e}")

        return response