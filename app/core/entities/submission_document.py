from beanie import Document
from typing import List, Optional
from pymongo import IndexModel
from datetime import date

class SubmissionDocument(Document):
    cik: str
    entity_type: str
    sic: str
    sic_description: str
    owner_org: str
    insider_transaction_for_owner_exists: int
    insider_transaction_for_issuer_exists: int
    name: str
    tickers: List[str]
    exchanges: List[str]
    ein: str
    # 타입 확인이 안됨, 일단 테이블은 string으로
    lei: None
    description: str
    website: str
    investor_website: str
    category: str
    fiscal_year_end: str
    state_of_incorporation: str
    state_of_incorporation_description: str
    addresses: dict
    phone: str
    flags: str
    former_names: List[dict]
    filings: dict
    ext_date: Optional[str] = date.today().isoformat()

    # 중복처리를 위한 Settings 오버라이드
    class Settings:
        name = "submission"
        indexes = [
            IndexModel(keys="filings", unique=True)
        ]
        ttl_seconds = 604800