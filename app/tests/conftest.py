# conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import MagicMock, AsyncMock
from collections.abc import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from main import app

# 비동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
# 그런데 최신 버전 FastAPI에서는 lifespan 설정을 권장하는데, AsyncClient를 사용할 경우 lifespan이 트리거 되지 않음
@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None, None]:
    async with AsyncClient(
          transport=ASGITransport(app=app),
          base_url="http://localhost:8002",
        ) as ac:
            yield ac

# 동기/비동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
# 최신 버전 FastAPI에서는 lifespan 설정을 권장하기에, 이쪽을 더 사용함
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
      with TestClient(app=app) as c:
            yield c

# api_caller Mock
@pytest.fixture(scope="module")
def mock_api_caller() -> MagicMock:
      mock_api_caller = MagicMock()
      return mock_api_caller

# edgar_service Mock
@pytest.fixture(scope="module")
def mock_edgar_service() -> MagicMock:
      mock_edgar_service = MagicMock()
      return mock_edgar_service

# paser_service Mock
@pytest.fixture(scope="module")
def mock_parser_service() -> MagicMock:
      mock_parser_service = MagicMock()
      return mock_parser_service

# massege_handler Mock
@pytest.fixture(scope="module")
def mock_message_handler() -> AsyncMock:
      mock_message_handler = AsyncMock()
      return mock_message_handler

# filings_usecase Mock
@pytest.fixture(scope="module")
def mock_filings_usecase() -> MagicMock:
      mock_filings_usecase = MagicMock()
      return mock_filings_usecase