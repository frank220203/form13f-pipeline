from typing import List, Optional
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
    async def get_all_tickers(
        self, 
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        모든 회사의 Ticker, CIK 정보 반환.
        """
        request_dto = FilingsRequestDto(email=email)
        tickers = await filings_usecase.get_all_tickers(request_dto.headers)

        return JSONResponse(content={"tickers": tickers}, status_code=status.HTTP_200_OK)
    
    @filings_router.get("/submissions")
    async def get_all_submissions(
        self, 
        cik: str = Query(..., description="10자리의 중앙 인덱스 키, ex) 0001067983"),
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        filing_type: List[str] = Query(None, description="문서유형, ex) 13F-HR"),
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        회사의 모든 제출물 반환
        """
        request_dto = FilingsRequestDto(email=email, params={'cik': cik, 'filing_type': filing_type})
        submissions = await filings_usecase.get_all_submissions(cik=request_dto.params["cik"], headers=request_dto.headers, filing_type=request_dto.params["filing_type"])
        
        return JSONResponse(content={"submissions": submissions}, status_code=status.HTTP_200_OK)
    
    @filings_router.get("/portfolio")
    async def get_portfolio(
        self,
        cik: str = Query(..., description="10자리의 중앙 인덱스 키, ex) 0001067983"),
        email: str = Query(..., description="SEC EDGAR의 정책으로 User-Agent로 회사 메일 요구"),
        accession_number: str = Query(..., description="접근번호, ex) 0000950123-25-005701"),
        filings_usecase: FilingsUsecase = Depends(get_filings_usecase)
    ) -> JSONResponse:
        """
        Portfolio Isseurs 반환.
        """
        request_dto = FilingsRequestDto(email=email, params={'cik': cik, 'accession_number': accession_number})
        portfolio = await filings_usecase.get_portfolio(cik=request_dto.params["cik"], headers=request_dto.headers, accession_number=request_dto.params["accession_number"])

        return JSONResponse(content={"porfolio": portfolio}, status_code=status.HTTP_200_OK)
    
    def get_router(self):
        return filings_router