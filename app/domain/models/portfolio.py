from typing import List
from pydantic import BaseModel, Field
from domain.models.issuer import Issuer

class Portfolio(BaseModel):
    header_data: dict = Field(alias='headerData')
    form_data: dict = Field(alias='formData')
    issuers: List[Issuer] = Field(..., description="보유 주식")