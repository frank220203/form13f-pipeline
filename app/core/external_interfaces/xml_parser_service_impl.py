import xmltodict
from domain.usecases.services.xml_parser_service import XmlPaserService

class XmlPaserServiceImpl(XmlPaserService):

    def xml_to_dict(self, data: str) -> dict:
        return xmltodict.parse(data)