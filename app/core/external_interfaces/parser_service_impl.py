import re
from bs4 import BeautifulSoup
from typing import List
from domain.usecases.services.parser_service import PaserService

class PaserServiceImpl(PaserService):

    def find_documents_urls(self, data:str) -> List[str]:
        # tag : table, tr, td, a // attribute : class, href
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', {'class': 'tableFile2'})
        # print(table)
        urls = []

        # 첫 번째 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                # 두 번째 td에 a태그 있음
                link = cols[1].find('a')['href']
                urls.append(link)

        return urls
    
    def find_portfolios(self, data: str) -> dict:
        # tag : table, tr, td, a // attribute : class, href
        soup = BeautifulSoup(data, 'html.parser')
        ## meta
        form = soup.find_all('div', class_= 'formGrouping')
        portfolio_meta = {}

        for f in form:
            for ih, i in zip(
                f.find_all('div', class_='infoHead'), 
                f.find_all('div', class_='info')
                ):
                portfolio_meta.update({ih.text: i.text})

        form = soup.find('span', class_= 'companyName')
        portfolio_meta.update({'cik': form.find('a').text[:9]})

        ## url
        table = soup.find('table', {'class': 'tableFile'})
        urls = []
        # 숫자.html 찾는 정규식
        pattern = r'^\d+\.html$'

        # 첫 번째 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                # 세 번째 td에 a태그 있음
                if re.match(pattern, cols[2].find('a').text):
                    # print(cols[2].find('a').text)
                    link = cols[2].find('a')['href']
                    # print(link)
                    urls.append(link)

        portfolios = {
            'meta': portfolio_meta,
            'urls': urls
            }
        
        # print(portfolios)

        return portfolios
    
    def find_portfolio_issuers(self, data: str, meta: str) -> List[dict]:
        # tag : table, tr, td, a // attribute : class, href
        soup = BeautifulSoup(data, 'html.parser')
        # 포트폴리오는 테이블에 class가 없고, 두 번째 테이블에 상장회사 정보가 담겨 있다.
        table = soup.find('table', {'summary': 'Form 13F-NT Header Information'})
        # print(table)
        issuers = [meta]

        # 1~3 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[3:]:
            cols = row.find_all('td')
            if len(cols) > 12:
                issuer = {
                    'name': cols[0].text,
                    'class_tilte': cols[1].text,
                    'cusip': cols[2].text,
                    'figi': cols[3].text.replace("\xa0", ""),
                    'value': cols[4].text,
                    'amount': cols[5].text,
                    'type': cols[6].text,
                    'put_call': cols[7].text.replace("\xa0", ""),
                    'investment_discretion': cols[8].text,
                    'other_manager': cols[9].text,
                    'votiong_authority': {'sole':cols[10].text, 'shared':cols[11].text, 'none':cols[12].text}
                    }
                issuers.append(issuer)
        # print(len(issuers))

        return issuers