import httpx
from typing import Optional
from domain.usecases.services.api_caller import ApiCaller

class HttpxClient(ApiCaller):

    async def call(
            self,
            url: str,
            headers: dict,
            params: Optional[dict] = None
    ) -> str:
        async with httpx.AsyncClient() as client:
            data = await client.get(url, headers=headers, params=params)
        return data.text