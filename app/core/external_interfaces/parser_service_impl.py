import re
from bs4 import BeautifulSoup
from typing import List
from domain.usecases.services.parser_service import PaserService

class PaserServiceImpl(PaserService):

    def find_documents_urls(self, data:str) -> List[str]:
        # tag : table, tr, td, a // attribute : class, href
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tableFile2'})
        print(table)
        urls = []

        # 첫 번째 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                # 두 번째 td에 a태그 있음
                link = cols[1].find('a')['href']
                urls.append(link)

        return urls
    
    def find_portfolios_urls(self, data:str) -> List[str]:
        # tag : table, tr, td, a // attribute : class, href
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tableFile'})
        print(table)
        urls = []
        # 숫자.html 찾는 정규식식
        pattern = r'^\d+\.html$'

        # 첫 번째 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                # 세 번째 td에 a태그 있음
                if re.match(pattern, cols[2].find('a').text):
                    print(cols[2].find('a').text)
                    link = cols[2].find('a')['href']
                    print(link)
                    urls.append(link)

        return urls