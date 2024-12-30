import pytest
from unittest.mock import MagicMock, AsyncMock
from domain.usecases.fillings_usecase import FillingsUsecase

# get_documents_urls 단위 테스트
@pytest.mark.anyio
async def test_get_documents_urls(
    mock_parser_service: MagicMock, 
    mock_edgar_api_service: MagicMock
    ) -> None:
    # Given & Mock
    mock_parser_service.find_documents_urls.return_value = ['url1', 'url2']
    mock_edgar_api_service.get_fillings_list = AsyncMock()
    mock_edgar_api_service.get_fillings_list.return_value = "<html><body><table class='tableFile2'><tr><th>Description</th></tr><tr><td>13F-HR</td><td><a href='url1'> Documents</a></td></tr><tr><td>13F-HR</td><td><a href='url2'> Documents</a></td></tr></table></body></html>"

    # When & Mocking
    fillings_usecase = FillingsUsecase(mock_parser_service, mock_edgar_api_service)
    urls = await fillings_usecase.get_documents_urls(email="sample@email.com", endpoint="/cgi-bin/browse-edgar/getcompany", cik="0001067983", type="13F-HR")

    # Then
    assert urls == ['url1', 'url2']

# get_portfolios_urls 단위 테스트
@pytest.mark.anyio
async def test_get_portfolios_urls(
    mock_parser_service: MagicMock, 
    mock_edgar_api_service: MagicMock   
) -> None:
    # Given & Mock
    mock_parser_service.find_portfolios_urls.return_value = ['url1', 'url2']
    mock_edgar_api_service.get_fillings_list = AsyncMock()
    mock_edgar_api_service.get_fillings_list.return_value = "<html><body><table class='tableFile'><tr><th>Description</th></tr><tr><td></td><td>13F-HR</td><td><a href='url1'> Documents</a></td></tr><tr><td></td><td>13F-HR</td><td><a href='url2'> Documents</a></td></tr></table></body></html>"

    # When & Mocking
    fillings_usecase = FillingsUsecase(mock_parser_service, mock_edgar_api_service)
    urls = await fillings_usecase.get_portfolios_urls(email="sample@email.com", endpoint="/Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm")