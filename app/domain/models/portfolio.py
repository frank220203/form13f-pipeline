from datetime import datetime
from pydantic import BaseModel, Field

class Portfolio(BaseModel):
    cik: str = Field(..., description="sec에 등록된 기업 고유 식별번호")
    name: str = Field(..., description="상장회사 이름")
    class_tilte: str = Field(..., description="주식 종류")
    cusip: str = Field(..., description="미국에서 사용하는 주식 고유 식별 번호")
    figi: str = Field(..., description="Bloomberg가 관리하는 금융 상품의 고유 식별자")
    value: float = Field(..., description="주식 가치")
    amount: float = Field(..., description="주식 수량")
    type: str = Field(..., description="SH : 주식 / PRN : 채권")
    put_call: str = Field(..., description="매매권리")
    investment_discretion: str = Field(..., description="투자 재량권")
    other_manager: str = Field(..., description="해당 주식 관리자")
    votiong_authority: dict = Field(..., description="투표권")
    filling_accepted: datetime = Field(..., description="제출날짜")
    report_period: datetime = Field(..., description="보고 분기")
    create_at: datetime = Field(..., description="데이터 생성날짜")