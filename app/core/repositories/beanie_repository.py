from typing import Optional
from beanie import init_beanie
from pydantic import BaseModel
from pymongo.asynchronous.database import AsyncDatabase
class BeanieRepository():

    def __init__(self):
        pass

    async def init_beanie(self, my_database: Optional[AsyncDatabase], model: BaseModel) -> None:
        await init_beanie(database=my_database, document_models=[model])