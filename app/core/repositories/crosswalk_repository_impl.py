from domain.models.crosswalk import Crosswalk
from core.entities.crosswalk_document import CrosswalkDocument
from domain.usecases.repositories.crosswalk_repository import CrosswalkRepository

class CrosswalkRepositoryImpl(CrosswalkRepository):

    async def add_data(self, crosswalk: Crosswalk) -> Crosswalk:
        crosswalk_doc = CrosswalkDocument(**crosswalk.model_dump())
        await crosswalk_doc.insert()
        return Crosswalk(**crosswalk_doc.model_dump())
    
    async def get_crosswalk_by_sin(self, sin: str) -> Crosswalk:
        crosswalk_doc = await CrosswalkDocument.find_one(sin)
        return Crosswalk(**crosswalk_doc.model_dump())