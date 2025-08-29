from typing import Optional
from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.header_data.filer_infos.filers.filer import Filer

class FilerInfo(BaseModel):
    live_test_flag: str = Field(..., alias=AliasChoices("liveTestFlag", "live_test_flag"))
    flags: Optional[str] = None
    filer: Filer
    period_of_report: str = Field(..., alias=AliasChoices("periodOfReport", "period_of_report"))