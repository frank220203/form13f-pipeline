from typing import Optional
from pydantic import BaseModel

class Ticker(BaseModel):
    cik: int
    name: str
    ticker: str
    exchange: Optional[str] = None