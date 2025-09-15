from pymongo.errors import DuplicateKeyError
from core.entities.crosswalk_document import CrosswalkDocument

from domain.models.crosswalk import Crosswalk
from domain.usecases.repositories.crosswalk_repository import CrosswalkRepository

class CrosswalkRepositoryImpl(CrosswalkRepository):

    async def add_data(self, crosswalk: Crosswalk) -> Crosswalk:
        crosswalk_doc = CrosswalkDocument(**crosswalk.model_dump())
        try:
            await crosswalk_doc.insert()
        except DuplicateKeyError:
            print("crosswalk_doc 중복")
            return None
            # 추후 도메인 계층에 예외 처리하는 로직 구현 필요
            # raise DomainModelException()
        return Crosswalk(**crosswalk_doc.model_dump())
    
    async def get_crosswalk_by_sin(self, crosswalk: Crosswalk) -> Crosswalk:
        crosswalk_doc = await CrosswalkDocument.find_one(CrosswalkDocument.sin == crosswalk.sin)
        if not crosswalk_doc:
            return None
        return Crosswalk(**crosswalk_doc.model_dump())