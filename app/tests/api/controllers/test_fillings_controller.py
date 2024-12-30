import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock
from main import app
from core.config.app_config import Settings
from api.deps.di_manager import get_fillings_usecase

settings = Settings()

# get_documents_urls 단위 테스트
@pytest.mark.anyio
async def test_get_documents_urls(
    async_client: AsyncClient,
    mock_fillings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_fillings_usecase.get_documents_urls = AsyncMock()
    mock_fillings_usecase.get_documents_urls.return_value = ["url1", "url2"]
    
    # Mocking
    app.dependency_overrides[get_fillings_usecase] = lambda: mock_fillings_usecase

    # When
    response = await async_client.get(f"{settings.API_V1_STR}/fillings/documents?endpoint=/cgi-bin/browse-edgar/getcompany&email=test@email.com&cik=0001067983")

    # Then
    assert response.status_code == 200
    assert response.json() == {"urls": ["url1", "url2"]}

# get_portfolios 단위 테스트
@pytest.mark.anyio
async def test_get_portfolios_urls(
    async_client: AsyncClient,
    mock_fillings_usecase: MagicMock
    ) -> None:
    # Mock
    mock_fillings_usecase.get_portfolios_urls = AsyncMock()
    mock_fillings_usecase.get_portfolios_urls.return_value = ["url1", "url2"]

    # Mocking
    app.dependency_overrides[get_fillings_usecase] = lambda: mock_fillings_usecase

    # When
    response = await async_client.get(f"{settings.API_V1_STR}/fillings/portfolios?email=sample@email.com&endpoint=/Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm")

    # Then
    assert response.status_code == 200
    assert response.json() == {"porfolios_urls": ["url1", "url2"]}