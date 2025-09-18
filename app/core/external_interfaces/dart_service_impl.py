from typing import List

from domain.config_manager import ConfigManager
from domain.usecases.services.dart_service import DartService

class DartServiceImpl(DartService):
    __api_key: str
    __corp_code_url: str

    def __init__(self, settings: ConfigManager):
        self.__api_key = settings.get_dart_api_key()
        self.__corp_code_url = settings.get_corp_code_url()

    def get_api_key(self) -> str:
        return self.__api_key

    def get_corp_code_url(self) -> str:
        url = f"{self.__corp_code_url}?crtfc_key={self.__api_key}"
        return url