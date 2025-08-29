from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.header_data.filer_infos.filer_info import FilerInfo

class HeaderData(BaseModel):
    submission_type: str = Field(..., alias=AliasChoices("submissionType", "submission_type"))
    filer_info: FilerInfo = Field(..., alias=AliasChoices("filerInfo", "filer_info"))