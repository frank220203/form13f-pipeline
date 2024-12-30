from typing import List, Optional

from domain.usecases.dto.fillings_request_dto import FillingsRequestDto
from domain.usecases.services.parser_service import PaserService
from domain.usecases.services.edgar_api_service import EdgarApiService

class FillingsUsecase:

    __paser_service: PaserService
    __edgar_api_service: EdgarApiService
    
    def __init__(self, paser_service: PaserService, edgar_api_service: EdgarApiService):
        self.__paser_service = paser_service
        self.__edgar_api_service = edgar_api_service

    async def get_documents_urls(
            self,
            email: str, 
            endpoint: str, 
            cik: Optional[str] = "", 
            type: Optional[str] = "", 
            owner: Optional[str] = "", 
            dateb: Optional[str] = "", 
            count: Optional[int] = 0, 
            search_text: Optional[str] = ""
    ) -> List[str]:
        request_dto = FillingsRequestDto(headers={'User-Agent': email}, params={'CIK': cik, 'type': type, 'owner': owner, 'dateb': dateb, 'count': count, 'search_text': search_text}, endpoint=endpoint)
        data = await self.__edgar_api_service.get_fillings_list(request_dto.url, request_dto.headers, request_dto.params)
        urls = self.__paser_service.find_documents_urls(data)
        return urls
        
    async def get_portfolios_urls(
            self,
            email: str,
            endpoint: str
    ) -> List[str]:
        request_dto = FillingsRequestDto(headers={'User-Agent': email}, params={}, endpoint=endpoint)
        data = await self.__edgar_api_service.get_fillings_list(request_dto.url, request_dto.headers, request_dto.params)
        urls = self.__paser_service.find_portfolios_urls(data)
        return urls