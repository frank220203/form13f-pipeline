# conftest.py
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from unittest.mock import MagicMock
from collections.abc import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from main import app, lifespan

# 비동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
# 그런데 최신 버전 FastAPI에서는 lifespan 설정을 권장하는데, AsyncClient를 사용할 경우 lifespan이 트리거 되지 않음
@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None, None]:
    async with AsyncClient(
          transport=ASGITransport(app=app),
          base_url="url",
        ) as ac:
            yield ac

# 동기/비동기 함수 테스트용 client (HTTP 요청 받은 것으로 간주)
# 최신 버전 FastAPI에서는 lifespan 설정을 권장하기에, 이쪽을 더 사용함
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
      with TestClient(app=app) as c:
            yield c

# 엔드포인트 호출 없이 비동기 함수 테스트하기 위해 pytest_asyncio 사용
# 직접 lifespan을 실행해서 app(혹은 app의 요소)을 넘겨줘야함.
@pytest_asyncio.fixture(scope="function")
async def kafka_service():
      async with lifespan(app) as ls:
            yield app.state.kafka_service

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
def mock_xml_parser_service() -> MagicMock:
      mock_xml_parser_service = MagicMock()
      return mock_xml_parser_service
@pytest.fixture(scope="module")
def mock_html_parser_service() -> MagicMock:
      mock_html_parser_service = MagicMock()
      return mock_html_parser_service

# massege_handler Mock
@pytest.fixture(scope="module")
def mock_message_handler() -> MagicMock:
      mock_message_handler = MagicMock()
      return mock_message_handler

# ticker_repository Mock
@pytest.fixture(scope="module")
def mock_ticker_repository() -> MagicMock:
      mock_ticker_repository = MagicMock()
      return mock_ticker_repository

# submission_repository Mock
@pytest.fixture(scope="module")
def mock_submission_repository() -> MagicMock:
      mock_submission_repository = MagicMock()
      return mock_submission_repository

# portfolio_repository Mock
@pytest.fixture(scope="module")
def mock_portfolio_repository() -> MagicMock:
      mock_portfolio_repository = MagicMock()
      return mock_portfolio_repository

# crosswalk_repository Mock
@pytest.fixture(scope="module")
def mock_crosswalk_repository() -> MagicMock:
      mock_crosswalk_repository = MagicMock()
      return mock_crosswalk_repository

# filings_usecase Mock
@pytest.fixture(scope="module")
def mock_filings_usecase() -> MagicMock:
      mock_filings_usecase = MagicMock()
      return mock_filings_usecase