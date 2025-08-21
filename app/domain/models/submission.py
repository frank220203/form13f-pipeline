from typing import List
from pydantic import BaseModel, Field

class Submission(BaseModel):
    cik: str
    # serialization_alias는 Validation 검사 X
    entity_type: str = Field(..., serialization_alias='entityType')
    sic: str
    sic_description: str = Field(..., serialization_alias='sicDescription')
    owner_org: str = Field(..., serialization_alias='ownerOrg')
    insider_transaction_for_owner_exists: int = Field(..., serialization_alias='insiderTransactionForOwnerExists')
    insider_transaction_for_issuer_exists: int = Field(..., serialization_alias='insiderTransactionForIssuerExists')
    name: str
    tickers: List[str]
    exchanges: List[str]
    # 타입 확인이 안됨, -> 2025-08-21 str으로 확인
    ein: str
    # 타입 확인이 안됨, 일단 테이블은 string으로
    lei: None
    description: str
    website: str
    investor_website: str = Field(..., serialization_alias='investorWebsite')
    category: str
    fiscal_year_end: str = Field(..., serialization_alias='fiscalYearEnd')
    state_of_incorporation: str = Field(..., serialization_alias='stateOfIncorporation')
    state_of_incorporation_description: str = Field(..., serialization_alias='stateOfIncorporationDescription')
    addresses: dict
    phone: str
    flags: str
    former_names: List[dict] = Field(..., serialization_alias='formerNames')
    filings: dict

    class Config:
        allow_population_by_field_name = True