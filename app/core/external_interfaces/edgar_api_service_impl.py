import httpx
from domain.usecases.services.edgar_api_service import EdgarApiService

class EdgarApiServiceImpl(EdgarApiService):

    def __init__(self):
        pass
        # cik 목록 url
        # self.api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
        

    async def get_fillings_list(
            self,
            url: str,
            headers: dict,
            params: dict
            ) -> str:
        
        async with httpx.AsyncClient() as client:
            data = await client.get(url, headers=headers, params=params)
        return data.text
        