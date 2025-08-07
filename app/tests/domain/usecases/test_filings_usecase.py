import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from domain.usecases.filings_usecase import FilingsUsecase

# get_all_tickers 단위 테스트
@pytest.mark.anyio
async def test_get_all_tickers(
    mock_api_caller: MagicMock,
    mock_edgar_service: MagicMock,
    mock_parser_service: MagicMock,
    mock_message_handler: MagicMock
) -> None:
    # Given & Mock
    mock_edgar_service.get_edgar_url.return_value = "https://www.test.com"
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = {
        'fields':[
            "cik",
            "name",
            "ticker",
            "exchange"
        ],
        'data':[[
            "1045810",
            "NVIDIA CORP",
            "NVDA",
            "Nasdaq"
        ]]
    }

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller,
        mock_edgar_service,
        mock_parser_service,
        mock_message_handler
    )

    tickers = await filings_usecase.get_all_tickers(headers={'User-Agent': "test@email.com"})

    # Then
    assert tickers == {
        'fields':[
            "cik",
            "name",
            "ticker",
            "exchange"
        ],
        'data':[[
            "1045810",
            "NVIDIA CORP",
            "NVDA",
            "Nasdaq"
            ]]
    }

# get_all_submissions 단위 테스트
@pytest.mark.anyio
async def test_get_all_submissions(
    mock_api_caller: MagicMock,
    mock_edgar_service: MagicMock,
    mock_parser_service: MagicMock,
    mock_message_handler: MagicMock
) -> None:
    # Given & Mock
    mock_edgar_service.get_all_submissions_url.return_value = "https://www.test.com"
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = {
        'cik':"0001067983", 
        'entityType':"operating",
        'sic':"6331",
        'sicDescription':"Fire, Marine",
        'ownerOrg':"02 Finance",
        'insiderTransactionForOwnerExists':1,
        'insiderTransactionForIssuerExists':1,
        'name':"BERKSHIRE HATHAWAY INC",
        'tickers':["BRK-B", "BRK-A"],
        'exchanges':["NYSE", "NYSE"],
        'ein':None,
        'lei':None,
        'description':"",
        'website':"",
        'investorWebsite':"",
        'category':"Large accelerated",
        'fiscalYearEnd':"1231",
        'stateOfIncorporation':"DE",
        'stateOfIncorporationDescription':"DE",
        'addresses':{'mailing':{
                'street1':"3555 FARNAM",
                'street2':None,
                'city':"OMAHA"
            }},
        'phone':"4023461400",
        'flags':"",
        'formerNames':[{
            'name':"NBH INC",
            'from':"1998-08-10",
            'to':"1999-01-05"
            }],
        'filings':{'recent':{
            'accessionNumber':[
                "0000950123-25-00570", 
                "0000950170-25-102306", 
                "0000950170-25-102303"
                ],
            'filingDate':[
                "2025-08-04",
                "2025-08-04",
                "2025-08-04"
                ],
            'reportDate':[
                "2025-07-31",
                "2025-07-31",
                "2025-07-31"
                ]
            }}
        }
    mock_edgar_service.find_submissions.return_value = {
        'cik':"0001067983", 
        'entityType':"operating",
        'sic':"6331",
        'sicDescription':"Fire, Marine",
        'ownerOrg':"02 Finance",
        'insiderTransactionForOwnerExists':1,
        'insiderTransactionForIssuerExists':1,
        'name':"BERKSHIRE HATHAWAY INC",
        'tickers':["BRK-B", "BRK-A"],
        'exchanges':["NYSE", "NYSE"],
        'ein':None,
        'lei':None,
        'description':"",
        'website':"",
        'investorWebsite':"",
        'category':"Large accelerated",
        'fiscalYearEnd':"1231",
        'stateOfIncorporation':"DE",
        'stateOfIncorporationDescription':"DE",
        'addresses':{'mailing':{
                'street1':"3555 FARNAM",
                'street2':None,
                'city':"OMAHA"
            }},
        'phone':"4023461400",
        'flags':"",
        'formerNames':[{
            'name':"NBH INC",
            'from':"1998-08-10",
            'to':"1999-01-05"
            }],
        'filings':{'recent':{
            'accessionNumber':[
                "0000950123-25-00570", 
                "0000950170-25-102306", 
                "0000950170-25-102303"
                ],
            'filingDate':[
                "2025-08-04",
                "2025-08-04",
                "2025-08-04"
                ],
            'reportDate':[
                "2025-07-31",
                "2025-07-31",
                "2025-07-31"
                ]
            }}
        }
    
    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller,
        mock_edgar_service,
        mock_parser_service,
        mock_message_handler
    )

    submissions = await filings_usecase.get_all_submissions(cik="0001067983", headers={'User-Agent': 'test@email.com'}, filings_type=["13F-HR", "13F-HR/A"])

    # Then
    assert submissions == {
        'cik':"0001067983", 
        'entityType':"operating",
        'sic':"6331",
        'sicDescription':"Fire, Marine",
        'ownerOrg':"02 Finance",
        'insiderTransactionForOwnerExists':1,
        'insiderTransactionForIssuerExists':1,
        'name':"BERKSHIRE HATHAWAY INC",
        'tickers':["BRK-B", "BRK-A"],
        'exchanges':["NYSE", "NYSE"],
        'ein':None,
        'lei':None,
        'description':"",
        'website':"",
        'investorWebsite':"",
        'category':"Large accelerated",
        'fiscalYearEnd':"1231",
        'stateOfIncorporation':"DE",
        'stateOfIncorporationDescription':"DE",
        'addresses':{'mailing':{
                'street1':"3555 FARNAM",
                'street2':None,
                'city':"OMAHA"
            }},
        'phone':"4023461400",
        'flags':"",
        'formerNames':[{
            'name':"NBH INC",
            'from':"1998-08-10",
            'to':"1999-01-05"
            }],
        'filings':{'recent':{
            'accessionNumber':[
                "0000950123-25-00570", 
                "0000950170-25-102306", 
                "0000950170-25-102303"
                ],
            'filingDate':[
                "2025-08-04",
                "2025-08-04",
                "2025-08-04"
                ],
            'reportDate':[
                "2025-07-31",
                "2025-07-31",
                "2025-07-31"
                ]
            }}
        }

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