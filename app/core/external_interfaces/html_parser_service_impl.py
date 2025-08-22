import re
from bs4 import BeautifulSoup
from domain.usecases.services.html_parser_service import HtmlPaserService

class HtmlPaserServiceImpl(HtmlPaserService):

    def find_xml(self, data: str) -> str:
        soup = BeautifulSoup(data, 'html.parser')
        xml_link = ""
        
        for a_tag in soup.find_all('a', href=re.compile(r'\.xml$')):
            link = a_tag.get('href')
            if "primary_doc" not in link:
                xml_link = link

        return xml_link