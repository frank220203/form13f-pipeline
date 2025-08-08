import xmltodict
from domain.usecases.services.parser_service import PaserService

class PaserServiceImpl(PaserService):

    def xml_to_dict(self, data: str) -> dict:
        return xmltodict.parse(data)