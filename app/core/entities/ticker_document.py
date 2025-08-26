from beanie import Document
from typing import Optional
from pymongo import IndexModel
from datetime import date

class TickerDocument(Document):
    cik: int
    name: str
    ticker: str
    exchange: Optional[str] = None
    ext_date: Optional[str] = date.today().isoformat()

    # 중복처리를 위한 Settings 오버라이드
    class Settings:
        name = "ticker"
        indexes = [
            IndexModel(keys="ticker", unique=True)
        ]