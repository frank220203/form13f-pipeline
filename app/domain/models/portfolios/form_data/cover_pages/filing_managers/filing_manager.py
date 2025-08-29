from pydantic import BaseModel, Field, AliasChoices
from domain.models.portfolios.form_data.cover_pages.filing_managers.address import Address

class FilingManager(BaseModel):
    name: str
    address: Address