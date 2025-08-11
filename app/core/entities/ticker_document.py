from typing import List
from beanie import Document

class Ticker(Document):
    fields: List[str]
    data: List[List[str]]