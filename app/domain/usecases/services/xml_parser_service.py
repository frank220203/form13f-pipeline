from abc import ABC, abstractmethod

class XmlPaserService(ABC):
    @abstractmethod
    def xml_to_dict(self, data: str) -> dict:
        pass