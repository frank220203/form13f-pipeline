import os
import requests
from dotenv import load_dotenv
from adapter.gateways.external_interfaces.edgar_api_client import EdgarApiClient

class EdgarApiClientImpl(EdgarApiClient):
    def __init__(self):
        self.api_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        load_dotenv(dotenv_path=f"{os.getcwd()}/src/infrastructure/env/.env")
        # cik 목록 url
        # self.api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
        

    def get_13f_data(self, cik: str = '0001067983', start: int = 0, count: int = 1):
        
        # 미국 증권거래위원회는 사용자 에이전트로 회사 도메인을 요구한다.
        user_agent = os.getenv("USER_AGENT")
        print(user_agent)
        headers = {"User-Agent": user_agent}

        params = {
            'action': 'getcompany',
            'CIK': cik,
            'type': '13F-HR',
            'owner': 'include',
            'count': count,
            'start': start,
            'output': 'json'
        }

        data = requests.get(self.api_url, headers=headers, params=params)
        print(data)

        return data.content.decode('utf-8')
        