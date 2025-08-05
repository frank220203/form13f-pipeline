import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from api.deps import di_manager
from api.deps.di_manager import get_filings_usecase
from main import app

config_manager = di_manager.get_config_manager()
api_version = config_manager.get_api_version()

# get_all_tickers 단위 테스트
@pytest.mark.anyio
async def test_get_all_tickers(
        client: TestClient,
        mock_filings_usecase: MagicMock
) -> None:
    #Mock
    mock_filings_usecase.get_all_tickers = AsyncMock()
    mock_filings_usecase.get_all_tickers.return_value = {"fields":["cik","name","ticker","exchange"],"data":[[1045810,"NVIDIA CORP","NVDA","Nasdaq"]]}
    
    # Mocking // 의존성 주입을 안 할 경우 실제 API를 타게 됨 (통합테스트 가능)
    app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    # TestClient 자체는 동기적으로 작동하기 때문에 await 쓰지 않음
    response = client.get(f"{api_version}/filings/tickers?endpoint=/files/company_tickers_exchange.json&email=test@email.com")

    # Then
    assert response.status_code == 200
    assert response.json() == {"tickers":{"fields":["cik","name","ticker","exchange"],"data":[[1045810,"NVIDIA CORP","NVDA","Nasdaq"]]}}
    
# get_documents_urls 단위 테스트
@pytest.mark.anyio
async def test_get_documents_urls(
    # async_client: AsyncClient,
    client: TestClient,
    mock_filings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_filings_usecase.get_documents_urls = AsyncMock()
    mock_filings_usecase.get_documents_urls.return_value = ["url1", "url2"]
    
    # Mocking // 의존성 주입을 안 할 경우 실제 API를 타게 됨 (통합테스트 가능)
    # app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    # TestClient 자체는 동기적으로 작동하기 때문에 await 쓰지 않음
    # response = await client.get(f"{api_version}/filings/documents?endpoint=/cgi-bin/browse-edgar/getcompany&email=test@email.com&cik=0001067983")
    response = client.get(f"{api_version}/filings/documents?endpoint=/cgi-bin/browse-edgar/getcompany&email=test@email.com&cik=0001067983")

    # Then
    assert response.status_code == 200
    assert response.json() == {"urls": ["url1", "url2"]}

# get_portfolios_urls 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio_urls(
    client: TestClient,
    mock_filings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_filings_usecase.get_portfolio_urls = AsyncMock()
    mock_filings_usecase.get_portfolio_urls.return_value = {'meta':'data', 'urls':['url1', 'url2']}

    # Mocking
    # app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    response = client.get(f"{api_version}/filings/portfolios/urls?email=sample@email.com&endpoint=/Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm")

    # Then
    assert response.status_code == 200
    assert response.json() == {"porfolios": {'meta':'data', 'urls':['url1', 'url2']}}

# get_portfolios_issuers 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio(
    client: TestClient,
    mock_filings_usecase: MagicMock
) -> None:
    # Mock
    meta = json.dumps({'meta':{"Filing Date":"2024-11-14","Accepted":"2024-11-14 16:05:04","Documents":"2","Period of Report":"2024-09-30","Effectiveness Date":"2024-11-14","cik":"000106798"}})
    mock_filings_usecase.get_portfolio_issuers = AsyncMock()
    mock_filings_usecase.get_portfolio_issuers.return_value = ["stock1", "stock2"]

    # Mocking
    # app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    response = client.get(f"{api_version}/filings/portfolios/issuers?email=sample@email.com&endpoint=/Archives/edgar/data/1067983/000095012324011775/xslForm13F_X02/36917.xml&meta={meta}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"porfolio_issuers": ["stock1", "stock2"]}