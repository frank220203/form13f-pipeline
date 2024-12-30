from typing import Optional
from starlette import status

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from api.deps.di_manager import get_fillings_usecase
from api.routes.base_routes import fillings_router

from domain.usecases.fillings_usecase import FillingsUsecase

@cbv(fillings_router)
class FillingsController:
    
    # FastAPI는 요청을 처리할 때 각 엔드포인트에서 필요한 의존성을 추출 // __init__에서 추출 불가
    @fillings_router.get("/documents")
    async def get_documents_urls(
        self,
        endpoint: str = Query(..., description="ex) /cgi-bin/browse-edgar/getcompany"),
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        cik: str = Query(..., description="10자리의 중앙 인덱스 키, ex) 0001067983"),
        type: Optional[str] = Query(None, description="문서유형, ex) 13F-HR"),
        owner: Optional[str] = Query(None, description="소유자"),
        dateb: Optional[str] = Query(None, description="end date"),
        count: Optional[int] = Query(None, description="개수, default) 10"),
        search_text: Optional[str] = Query(None, description="특정 단어 검색"),
        fillings_usecase: FillingsUsecase = Depends(get_fillings_usecase)
    ) -> JSONResponse:
        """
        Documents URLS 반환.
        """
        urls = await fillings_usecase.get_documents_urls(endpoint, email, cik, type, owner, dateb, count, search_text)

        return JSONResponse(content={"urls": urls}, status_code=status.HTTP_200_OK)
    
    @fillings_router.get("/portfolios")
    async def get_portfolios_urls(
        self,
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        endpoint: str = Query(..., description="ex) /Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm"),
        fillings_usecase: FillingsUsecase = Depends(get_fillings_usecase)
    ) -> JSONResponse:
        """
        Portfolio URL 반환.
        """

        urls = await fillings_usecase.get_portfolios_urls(email, endpoint)

        return JSONResponse(content={"porfolios_urls": urls}, status_code=status.HTTP_200_OK)
    
    def get_router(self):
        return fillings_router
