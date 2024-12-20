from typing import Optional
from starlette import status

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from api.routes.base_routes import fillings_router
from api.gateways.external_interfaces.edgar_api_client_di import EdgarApiClientDi
from domain.usecase.fillings_usecase import FillingsUsecase

@cbv(fillings_router)
class FillingsController:
    
    def __init__(self):
        self.__fillings_usecase = FillingsUsecase()
    
    @fillings_router.get("/")
    async def get_documents_urls(
        self,
        action: Optional[str] = Query(None, description="ex) getcompany"),
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        cik: str = Query(..., description="10자리의 중앙 인덱스 키, ex) 0001067983"),
        type: Optional[str] = Query(None, description="문서유형, ex) 13F-HR"),
        owner: Optional[str] = Query(None, description="소유자"),
        dateb: Optional[str] = Query(None, description="end date"),
        count: Optional[int] = Query(None, description="개수, default) 10"),
        search_text: Optional[str] = Query(None, description="특정 단어 검색"),
        client_di: EdgarApiClientDi = Depends()
    ) -> JSONResponse:
        """
        Documents URLS 반환.
        """
        # FastAPI는 요청을 처리할 때 각 엔드포인트에서 필요한 의존성을 추출 // __init__에서 추출 불가
        client = client_di.get_edgar_api_client()
        request_dto = self.__fillings_usecase.get_request(action, email, cik, type, owner, dateb, count, search_text)
        data = await client.get_fillings_list(request_dto.url, request_dto.headers, request_dto.params)
        urls = self.__fillings_usecase.get_documents_urls(data)

        return JSONResponse(content={"message": urls}, status_code=status.HTTP_200_OK)
    
    def get_router(self):
        return fillings_router
