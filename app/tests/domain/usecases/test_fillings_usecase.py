import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from domain.usecases.filings_usecase import FilingsUsecase

# get_documents_urls 단위 테스트
@pytest.mark.anyio
async def test_get_documents_urls(
    mock_api_caller: MagicMock,
    mock_parser_service: MagicMock, 
    mock_message_handler: MagicMock
    ) -> None:
    # Given & Mock
    mock_parser_service.find_documents_urls.return_value = ['url1', 'url2']
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = "<html><body><table class='tableFile2'><tr><th>Description</th></tr><tr><td>13F-HR</td><td><a href='url1'> Documents</a></td></tr><tr><td>13F-HR</td><td><a href='url2'> Documents</a></td></tr></table></body></html>"

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller, 
        mock_parser_service, 
        mock_message_handler
        )
    urls = await filings_usecase.get_documents_urls(email="sample@email.com", endpoint="/cgi-bin/browse-edgar/getcompany", cik="0001067983", type="13F-HR")

    # Then
    assert urls == ['url1', 'url2']

# get_portfolios_urls 단위 테스트
@pytest.mark.anyio
async def test_get_portfolios(
    mock_api_caller: MagicMock,
    mock_parser_service: MagicMock, 
    mock_message_handler: MagicMock
) -> None:
    # Given & Mock
    mock_parser_service.find_portfolios.return_value = {'meta':'data', 'urls':['url1', 'url2']}
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = "<html><body><table class='tableFile'><tr><th>Description</th></tr><tr><td></td><td>13F-HR</td><td><a href='url1'> Documents</a></td></tr><tr><td></td><td>13F-HR</td><td><a href='url2'> Documents</a></td></tr></table></body></html>"

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller, 
        mock_parser_service, 
        mock_message_handler
        )
    protfolios = await filings_usecase.get_portfolios(email="sample@email.com", endpoint="/Archives/edgar/data/1067983/000095012324011775/0000950123-24-011775-index.htm")

    # Then
    assert protfolios == {'meta':'data', 'urls':['url1', 'url2']}

# get_portfolio_issers 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio_issuers(
    mock_api_caller: MagicMock,
    mock_parser_service: MagicMock, 
    mock_message_handler: MagicMock
) -> None:
    # Given & Mock
    meta = json.dumps({'meta':'data'})
    mock_parser_service.find_portfolio_issuers.return_value = ['stock1', 'stock2']
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = "<html><body><table class='tableFile'><tr><th>Description</th></tr><tr><td></td><td>13F-HR</td><td><a href='url1'> Documents</a></td></tr><tr><td></td><td>13F-HR</td><td><a href='url2'> Documents</a></td></tr></table></body></html>"

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller, 
        mock_parser_service, 
        mock_message_handler
        )
    urls = await filings_usecase.get_portfolio_issuers(
        meta=meta, 
        email="sample@email.com", 
        endpoint="/Archives/edgar/data/1067983/000095012324011775/xslForm13F_X02/36917.xml"
        )

    # Then
    assert urls == ['stock1', 'stock2']