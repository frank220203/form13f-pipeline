# conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import MagicMock
from collections.abc import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from main import app

# 비동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None, None]:
    async with AsyncClient(
          transport=ASGITransport(app=app),
          base_url="http://localhost:8002"
        ) as c:
            yield c

# 동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
      with TestClient(app) as c:
            yield c

# kafka_service Mock
@pytest.fixture(scope="module")
def mock_kafka_service() -> MagicMock:
      mock_kafka_service = MagicMock()
      return mock_kafka_service

# paser_service Mock
@pytest.fixture(scope="module")
def mock_parser_service() -> MagicMock:
      mock_parser_service = MagicMock()
      return mock_parser_service

# edgar_api_service Mock
@pytest.fixture(scope="module")
def mock_edgar_api_service() -> MagicMock:
      mock_edgar_api_service = MagicMock()
      return mock_edgar_api_service

# fillings_usecase Mock
@pytest.fixture(scope="module")
def mock_fillings_usecase() -> MagicMock:
      mock_fillings_usecase = MagicMock()
      return mock_fillings_usecase