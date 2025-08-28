from pydantic import BaseModel, Field, AliasChoices

class FormerName(BaseModel):
    name: str
    start: str = Field(..., alias=AliasChoices('from', 'start'))
    to: str
