from typing import List
from pydantic import BaseModel

class Ticker(BaseModel):
    fields: List[str]
    data: List[List[str]]