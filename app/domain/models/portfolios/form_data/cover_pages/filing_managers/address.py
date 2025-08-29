from pydantic import BaseModel, Field, AliasChoices

class Address(BaseModel):
    ns1_street1: str = Field(..., alias=AliasChoices("ns1:street1", "ns1_street1"))
    ns1_city: str  = Field(..., alias=AliasChoices("ns1:city", "ns1_city"))
    ns1_state_or_country: str  = Field(..., alias=AliasChoices("ns1:stateOrCountry", "ns1_state_or_country"))
    ns1_zip_code: str  = Field(..., alias=AliasChoices("ns1:zipCode", "ns1_zip_code"))