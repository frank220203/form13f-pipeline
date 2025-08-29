from pydantic import BaseModel

class Credential(BaseModel):
    cik: str
    ccc: str