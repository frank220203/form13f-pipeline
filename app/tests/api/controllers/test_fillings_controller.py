import json
import pytest

from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from api.deps import di_manager
from api.deps.di_manager import get_fillings_usecase
from main import app

config_manager = di_manager.get_config_manager()
api_version = config_manager.get_api_version()

# get_documents_urls 단위 테스트
@pytest.mark.anyio
async def test_get_documents_urls(
    # async_client: AsyncClient,
    client: TestClient,
    mock_fillings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_fillings_usecase.get_documents_urls = AsyncMock()
    mock_fillings_usecase.get_documents_urls.return_value = ["url1", "url2"]
    
    # Mocking // 의존성 주입을 안 할 경우 실제 API를 타게 됨 (통합테스트 가능)
    app.dependency_overrides[get_fillings_usecase] = lambda: mock_fillings_usecase

    # When
    # TestClient 자체는 동기적으로 작동하기 때문에 await 쓰지 않음
    # response = await client.get(f"{api_version}/fillings/documents?endpoint=/cgi-bin/browse-edgar/getcompany&email=test@email.com&cik=0001067983")
    response = client.get(f"{api_version}/fillings/documents?endpoint=/cgi-bin/browse-edgar/getcompany&email=test@email.com&cik=0001067983")

    # Then
    assert response.status_code == 200
    assert response.json() == {"urls": ["url1", "url2"]}

# get_portfolios_urls 단위 테스트
@pytest.mark.anyio
async def test_get_portfolios(
    client: TestClient,
    mock_fillings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_fillings_usecase.get_portfolios = AsyncMock()
    mock_fillings_usecase.get_portfolios.return_value = {'meta':'data', 'urls':['url1', 'url2']}

    # Mocking
    app.dependency_overrides[get_fillings_usecase] = lambda: mock_fillings_usecase

    # When
    response = client.get(f"{api_version}/fillings/portfolios?email=sample@email.com&endpoint=/Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm")

    # Then
    assert response.status_code == 200
    assert response.json() == {"porfolios": {'meta':'data', 'urls':['url1', 'url2']}}

# get_portfolios_issuers 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio_issuers(
    client: TestClient,
    mock_fillings_usecase: MagicMock
) -> None:
    # Mock
    meta = json.dumps({'meta':'data'})
    mock_fillings_usecase.get_portfolio_issuers = AsyncMock()
    mock_fillings_usecase.get_portfolio_issuers.return_value = ["stock1", "stock2"]

    # Mocking
    # app.dependency_overrides[get_fillings_usecase] = lambda: mock_fillings_usecase

    # When
    response = client.get(f"{api_version}/fillings/portfolio/issuers?email=sample@email.com&endpoint=/Archives/edgar/data/1067983/000095012324011775/xslForm13F_X02/36917.xml&meta={meta}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"porfolio_issuers": ["stock1", "stock2"]}