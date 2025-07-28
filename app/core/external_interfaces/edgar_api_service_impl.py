import httpx
from domain.usecases.services.api_caller import ApiCaller

class EdgarApiServiceImpl(ApiCaller):

    def __init__(self):
        pass
        # cik 목록 url
        # self.api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
        

    async def call(
            self,
            url: str,
            headers: dict,
            params: dict
            ) -> str:
        
        async with httpx.AsyncClient() as client:
            data = await client.get(url, headers=headers, params=params)
        return data.text