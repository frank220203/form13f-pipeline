from pydantic import BaseModel, Field, AliasChoices

class SignatureBlock(BaseModel):
    name: str
    title: str
    phone: str
    signature: str
    city: str
    state_or_country: str = Field(..., alias=AliasChoices("stateOrCountry", "state_or_country"))
    signature_date: str = Field(..., alias=AliasChoices("signatureDate", "signature_date"))