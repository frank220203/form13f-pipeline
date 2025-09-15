from typing import Optional
from pydantic import BaseModel, Field

class Crosswalk(BaseModel):
    sin: str = Field(..., description="증권 식별 번호 ex) cusip, isin")
    name: Optional[str] = None
    naics: Optional[str] = None
    industry: Optional[str] = None