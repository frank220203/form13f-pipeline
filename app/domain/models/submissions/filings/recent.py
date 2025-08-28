from typing import List
from pydantic import BaseModel, Field, AliasChoices, ConfigDict

class Recent(BaseModel):
    form: List[str]
    accession_number: List[str] = Field(..., alias=AliasChoices('accessionNumber', 'accession_number'))
    filing_date: List[str]  = Field(..., alias=AliasChoices('filingDate', 'filing_date'))
    report_date: List[str] = Field(..., alias=AliasChoices('reportDate', 'report_date'))
    acceptance_date_time: List[str]  = Field(..., alias=AliasChoices('acceptanceDateTime', 'acceptance_date_time'))

    # class에 선언된 필드만 가져오고 Dict의 나머지 필드 제외
    model_config = ConfigDict(extra="ignore")