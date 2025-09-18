from abc import ABC, abstractmethod

class DartService(ABC):
    @abstractmethod
    def get_api_key(self) -> str:
        pass
    @abstractmethod
    def get_corp_code_url(self) -> str:
        pass