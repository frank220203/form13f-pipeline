from fastapi import APIRouter

# controller에서 APIRouter를 생성 안할 수 있게 따로 관리해주는 용도
filings_router = APIRouter(prefix="/filings", tags=["filings"])