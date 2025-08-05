from typing import Optional
from starlette import status

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from api.deps.di_manager import get_filings_usecase
from api.routes.base_routes import filings_router
from api.dto.filings_request_dto import FilingsRequestDto

from domain.usecases.filings_usecase import FilingsUsecase

@cbv(filings_router)
class FilingsController:
    
    # FastAPI는 요청을 처리할 때 각 엔드포인트에서 필요한 의존성을 추출 // __init__에서 추출 불가
    @filings_router.get("/tickers")
    async def get_all_tickers(self, email:str, endpoint:str, filings_usecase: FilingsUsecase = Depends(get_filings_usecase)) -> JSONResponse:
        """
        모든 회사의 Ticker, CIK 정보 반환.
        """
        reqeust_dto = FilingsRequestDto(email=email, endpoint=endpoint)
        tickers = await filings_usecase.get_all_tickers(reqeust_dto.endpoint, reqeust_dto.headers)

        return JSONResponse(content={"tickers": tickers}, status_code=status.HTTP_200_OK)
    
    @filings_router.get("/documents")
    async def get_documents_urls(
        self,
        cik: str = Query(..., description="10자리의 중앙 인덱스 키, ex) 0001067983"),
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        endpoint: str = Query(..., description="ex) /cgi-bin/browse-edgar/getcompany"),
        type: Optional[str] = Query(None, description="문서유형, ex) 13F-HR"),
        owner: Optional[str] = Query(None, description="소유자"),
        dateb: Optional[str] = Query(None, description="end date"),
        count: Optional[int] = Query(None, description="개수, default) 10"),
        search_text: Optional[str] = Query(None, description="특정 단어 검색"),
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        Documents URLs 반환.
        """
        request_dto = FilingsRequestDto(
            email=email,
            endpoint=endpoint,
            params={
                'cik': cik,
                'type': type,
                'owner': owner,
                'dateb': dateb,
                'count': count,
                'search_text': search_text
            }
        )
        urls = await filings_usecase.get_documents_urls(request_dto.endpoint, request_dto.headers, request_dto.params)

        return JSONResponse(content={"urls": urls}, status_code=status.HTTP_200_OK)
    
    @filings_router.get("/portfolios/urls")
    async def get_portfolio_urls(
        self,
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        endpoint: str = Query(..., description="ex) /Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm"),
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        Portfolios URLs 반환.
        """
        porfolio_urls = await filings_usecase.get_portfolio_urls(request_dto.endpoint, request_dto.headers)

        return JSONResponse(content={"porfolio_urls": porfolio_urls}, status_code=status.HTTP_200_OK)
    
    @filings_router.get("/portfolios/issuers")
    async def get_portfolio(
        self,
        request_dto: FilingsRequestDto,
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        Portfolio Isseurs 반환.
        """
        portfolio = await filings_usecase.get_portfolio(request_dto.endpoint, request_dto.headers, request_dto.meta)

        return JSONResponse(content={"porfolio": portfolio}, status_code=status.HTTP_200_OK)
    
    def get_router(self):
        return filings_router