from typing import List
from pydantic import BaseModel, Field
from domain.models.issuer import Issuer

class Portfolio(BaseModel):
    cik: str = Field(..., description="sec에만 등록된 기업 고유 식별번호")
    filing_accepted: str = Field(..., description="제출날짜")
    report_period: str = Field(..., description="보고 분기")
    create_at: str = Field(..., description="데이터 생성날짜")
    issuers: List[Issuer] = Field(..., description="보유 주식")