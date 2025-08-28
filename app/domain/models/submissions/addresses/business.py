from typing import Optional
from pydantic import BaseModel, Field, AliasChoices

class Business(BaseModel):
    street1: str
    street2: Optional[str] = None
    city: str
    state_or_country: str = Field(..., alias=AliasChoices('stateOrCountry', 'state_or_country'))
    zip_code: str = Field(..., alias=AliasChoices('zipCode', 'zip_code'))
    state_or_country_description: str = Field(..., alias=AliasChoices('stateOrCountryDescription', 'state_or_country_description'))
    is_foreign_location: Optional[int] = Field(None, alias=AliasChoices('isForeignLocation', 'is_foreign_location'))
    foreign_state_territory: Optional[str] = Field(None, alias=AliasChoices('foreignStateTerritory', 'foreign_state_territory'))
    country: Optional[str] = None
    country_code: Optional[str] = Field(None, alias=AliasChoices('countryCode', 'country_code'))