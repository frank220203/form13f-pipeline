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
            # IP 주소로 API를 호출하는 경우
            # data = await client.get("http://217.189.34.109:8000/items/1")
            # 기본적으로는 도메인 주소로 API를 호출
            data = await client.get(url, headers=headers, params=params)
        return data.text
