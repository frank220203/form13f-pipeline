import importlib
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from domain.db_manager import DbManager
from domain.config_manager import ConfigManager

class BeanieRepository(DbManager):

    def __init__(self, settings: ConfigManager):
        self.__client = AsyncIOMotorClient(settings.get_mongo_db_url())
        self.__settings = settings

    async def init_db(self) -> None:
        model_paths = [path.strip() for path in self.__settings.get_document_models().split(',')]
        models = []
        
        for path in model_paths:
            try:
                module_path, class_name = path.rsplit('.', 1)
                module = importlib.import_module(module_path)
                model_class = getattr(module, class_name)
                models.append(model_class)
            except (ImportError, AttributeError, ValueError) as e:
                raise RuntimeError(f"Failed to dynamically load model from path: '{path}'") from e
            
        await init_beanie(database=self.__client.pipeline, document_models=models)