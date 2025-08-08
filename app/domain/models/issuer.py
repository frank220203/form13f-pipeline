from pydantic import BaseModel, Field

class Issuer(BaseModel):
    name_of_issuer: str = Field(..., alias='nameOfIssuer', description="상장회사 이름")
    tilte_of_class: str = Field(..., alias='titleOfClass', description="주식 종류")
    cusip: str = Field(..., description="미국에서 사용하는 주식 고유 식별 번호/국내도 형식만 다를 뿐, 동일")
    value: str = Field(..., description="주식 가치")
    shrs_or_prn_amt: dict = Field(..., alias='shrsOrPrnAmt', description="sshPrnamt : 주식 수량 / sshPrnamtType: SH(주식), PRN(채권)")
    investment_discretion: str = Field(..., alias='investmentDiscretion', description="투자 재량권")
    other_manager: str = Field(..., description="해당 주식 관리자")
    voting_authority: dict = Field(..., description="투표권")