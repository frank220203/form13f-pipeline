from pydantic import BaseModel, Field

class Issuer(BaseModel):
    name: str = Field(..., description="상장회사 이름")
    class_tilte: str = Field(..., description="주식 종류")
    cusip: str = Field(..., description="미국에서 사용하는 주식 고유 식별 번호/국내도 형식만 다를 뿐, 동일")
    figi: str = Field(..., description="Bloomberg가 관리하는 금융 상품의 고유 식별자")
    value: str = Field(..., description="주식 가치")
    amount: str = Field(..., description="주식 수량")
    type: str = Field(..., description="SH : 주식 / PRN : 채권")
    put_call: str = Field(..., description="매매권리")
    investment_discretion: str = Field(..., description="투자 재량권")
    other_manager: str = Field(..., description="해당 주식 관리자")
    votiong_authority: dict = Field(..., description="투표권")