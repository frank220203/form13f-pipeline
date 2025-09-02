from beanie import Document
from pymongo import IndexModel

class CrosswalkDocument(Document):
    sin: str
    naics: str

    class Settings:
        name = "crosswalk"
        indexes = [
            IndexModel(keys="sin", unique=True)
        ]