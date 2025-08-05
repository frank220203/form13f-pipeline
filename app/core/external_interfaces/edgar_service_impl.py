import httpx
from edgar import Company
from typing import Optional
from core.config import Settings
from domain.usecases.services.edgar_service import EdgarService

class EdgarServiceImpl(EdgarService):

    __url: str

    def __init__(self, settings: Settings):
        self.__url = settings.get_sec_url()
        pass
        # cik 목록 url
        # self.api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
        
    def get_edgar_url(self) -> str:
        return self.__url
    
    async def get_all_filings(self, cik, filing_type):
        return await super().get_all_filings(cik, filing_type)