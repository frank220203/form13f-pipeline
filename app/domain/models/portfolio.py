from typing import List
from pydantic import BaseModel, Field, AliasChoices
from domain.models.issuer import Issuer

class Portfolio(BaseModel):
    header_data: dict = Field(alias=AliasChoices('headerData', 'header_data'))
    form_data: dict = Field(alias=AliasChoices('formData', 'form_data'))
    issuers: List[Issuer] = Field(..., description="보유 주식")