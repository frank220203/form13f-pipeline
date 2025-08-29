from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.summary_pages.other_manager2_infos.other_manager2s.other_manager import OtherManager

class OtherManager2(BaseModel):
    sequence_number: str = Field(..., alias=AliasChoices("sequenceNumber", "sequence_number"))
    other_manager: OtherManager = Field(..., alias=AliasChoices("otherManager", "other_manager"))