from typing import List
from pydantic import BaseModel, Field, AliasChoices

class Submission(BaseModel):
    cik: str
    # AliasChoices로 두 가지 유형 모두 허용
    entity_type: str = Field(..., alias=AliasChoices('entityType', 'entity_type'))
    sic: str
    sic_description: str = Field(..., alias=AliasChoices('sicDescription', 'sic_description'))
    owner_org: str = Field(..., alias=AliasChoices('ownerOrg', 'owner_org'))
    insider_transaction_for_owner_exists: int = Field(..., alias=AliasChoices('insiderTransactionForOwnerExists', 'insider_transaction_for_owner_exists'))
    insider_transaction_for_issuer_exists: int = Field(..., alias=AliasChoices('insiderTransactionForIssuerExists', 'insider_transaction_for_issuer_exists'))
    name: str
    tickers: List[str]
    exchanges: List[str]
    # 타입 확인이 안됨, -> 2025-08-21 str으로 확인
    ein: str
    # 타입 확인이 안됨, 일단 테이블은 string으로
    lei: None
    description: str
    website: str
    investor_website: str = Field(..., alias=AliasChoices('investorWebsite', 'investor_website'))
    category: str
    fiscal_year_end: str = Field(..., alias=AliasChoices('fiscalYearEnd', 'fiscal_year_end'))
    state_of_incorporation: str = Field(..., alias=AliasChoices('stateOfIncorporation', 'state_of_incorporation'))
    state_of_incorporation_description: str = Field(..., alias=AliasChoices('stateOfIncorporationDescription', 'state_of_incorporation_description'))
    addresses: dict
    phone: str
    flags: str
    former_names: List[dict] = Field(..., alias=AliasChoices('formerNames', 'former_names'))
    filings: dict