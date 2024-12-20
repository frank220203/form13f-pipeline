from bs4 import BeautifulSoup
from typing import List

from domain.usecase.dto.fillings_request_dto import FillingsRequestDto

class FillingsUsecase():

    def get_request(
            self,
            action: str, 
            email: str, 
            cik: str, 
            type: str, 
            owner: str, 
            dateb: str, 
            count: int, 
            search_text: str
    ) -> FillingsRequestDto:
        return FillingsRequestDto(headers={'User-Agent': email}, params={'action': action, 'CIK': cik, 'type': type, 'owner': owner, 'dateb': dateb, 'count': count, 'search_text': search_text})
        
    def get_documents_urls(self, data: str) -> List[str]:
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find('table', {'class': 'tableFile2'})
        urls = []

        # 첫 번째 행은 헤더이므로 제외, tr내부 요소를 배열로 받음
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 0:
                print(cols)
                link = cols[1].find('a')['href']
                print(link)
                urls.append(link)

        return urls