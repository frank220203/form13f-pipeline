from pydantic import BaseModel, Field

class FormerName(BaseModel):
    name: str
    start: str = Field(..., alias='from')
    to: str
