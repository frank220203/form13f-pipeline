from typing import List
from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from domain.models.portfolios.issuer import Issuer
from domain.models.portfolios.form_data.form_data import FormData
from domain.models.portfolios.header_data.header_data import HeaderData

class Portfolio(BaseModel):
    header_data: HeaderData = Field(alias=AliasChoices('headerData', 'header_data'))
    form_data: FormData = Field(alias=AliasChoices('formData', 'form_data'))
    issuers: List[Issuer] = Field(..., description="보유 주식")