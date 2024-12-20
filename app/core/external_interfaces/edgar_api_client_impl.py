import httpx
from api.gateways.external_interfaces.edgar_api_client import EdgarApiClient
from core.config.app_config import Settings

class EdgarApiClientImpl(EdgarApiClient):

    __settings : Settings

    def __init__(self):
        self.__settings = Settings()
        # cik 목록 url
        # self.api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
        

    async def get_fillings_list(
            self,
            url: str,
            headers: dict,
            params: dict
            ):
        
        # 삭제 예정
        headers.update({'User-Agent': self.__settings.USER_AGENT})
        async with httpx.AsyncClient() as client:
            data = await client.get(url, headers=headers, params=params)
        return data
        