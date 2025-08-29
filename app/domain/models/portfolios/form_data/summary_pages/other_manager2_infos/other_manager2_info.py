from typing import List
from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.summary_pages.other_manager2_infos.other_manager2s.other_manager2 import OtherManager2

class OtherManager2Info(BaseModel):
    other_manager2: List[OtherManager2] = Field(..., alias=AliasChoices("otherManager2", "other_manager2"))