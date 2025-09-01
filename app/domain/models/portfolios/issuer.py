from pydantic import BaseModel, Field, AliasChoices

class Issuer(BaseModel):
    name_of_issuer: str = Field(..., alias=AliasChoices('nameOfIssuer', 'name_of_issuer'), description="상장회사 이름")
    title_of_class: str = Field(..., alias=AliasChoices('titleOfClass', 'title_of_class'), description="주식 종류")
    cusip: str = Field(..., description="미국에서 사용하는 주식 고유 식별 번호/국내는 ISIN 사용")
    value: str = Field(..., description="주식 가치")
    shrs_or_prn_amt: dict = Field(..., alias=AliasChoices('shrsOrPrnAmt', 'shrs_or_prn_amt'), description="sshPrnamt : 주식 수량 / sshPrnamtType: SH(주식), PRN(채권)")
    investment_discretion: str = Field(..., alias=AliasChoices('investmentDiscretion', 'investment_discretion'), description="투자 재량권")
    other_manager: str = Field(..., alias=AliasChoices('otherManager', 'other_manager'), description="해당 주식 관리자")
    voting_authority: dict = Field(..., alias=AliasChoices('votingAuthority', 'voting_authority'), description="투표권")