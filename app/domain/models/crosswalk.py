from pydantic import BaseModel, Field

class Crosswalk(BaseModel):
    sin: str = Field(..., description="증권 식별 번호 ex) cusip, isin")
    naisc: str