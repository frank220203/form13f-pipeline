from typing import List
from pydantic import BaseModel, Field

class Submission(BaseModel):
    cik: str
    entity_type: str = Field(alias='entityType')
    sic: str
    sic_description: str = Field(alias='sicDescription')
    owner_org: str = Field(alias='ownerOrg')
    insider_transaction_for_owner_exists: int = Field(alias='insiderTransactionForOwnerExists')
    insider_transaction_for_issuer_exists: int = Field(alias='insiderTransactionForIssuerExists')
    name: str
    tickers: List[str]
    exchanges: List[str]
    # 타입 확인이 안됨, 일단 테이블은 string으로
    ein: None
    # 타입 확인이 안됨, 일단 테이블은 string으로
    lei: None
    description: str
    website: str
    investor_website: str = Field(alias='investorWebsite')
    category: str
    fiscal_year_end: str = Field(alias='fiscalYearEnd')
    state_of_incorporation: str = Field(alias='stateOfIncorporation')
    state_of_incorporation_description: str = Field(alias='stateOfIncorporationDescription')
    addresses: dict
    phone: str
    flags: str
    former_names: List[dict] = Field(alias='formerNames')
    filings: dict