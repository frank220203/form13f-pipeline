from abc import ABC, abstractmethod

class HtmlPaserService(ABC):
    @abstractmethod
    def find_xml(self, data: str) -> str:
        pass