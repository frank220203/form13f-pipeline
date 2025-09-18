import json
import pytest
from unittest.mock import MagicMock, AsyncMock

from domain.models.submissions.submission import Submission
from domain.usecases.filings_usecase import FilingsUsecase

# get_all_tickers 단위 테스트
@pytest.mark.anyio
async def test_get_all_tickers(
    mock_api_caller: MagicMock,
    mock_edgar_service: MagicMock,
    mock_message_handler: MagicMock,
    mock_xml_parser_service: MagicMock,
    mock_html_parser_service: MagicMock
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
    mock_message_handler.publish = AsyncMock()

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller,
        mock_edgar_service,
        mock_message_handler,
        mock_xml_parser_service,
        mock_html_parser_service
    )

    tickers = await filings_usecase.get_all_tickers(headers={'User-Agent': "test@email.com"})

    # Then
    assert tickers == mock_api_caller.call.return_value

# get_all_submissions 단위 테스트
@pytest.mark.anyio
async def test_get_all_submissions(
    mock_api_caller: MagicMock,
    mock_edgar_service: MagicMock,
    mock_message_handler: MagicMock,
    mock_xml_parser_service: MagicMock,
    mock_html_parser_service: MagicMock
) -> None:
    # Given & Mock
    mock_edgar_service.get_all_submissions_url.return_value = "https://www.test.com"
    mock_response = {
        'cik':"0001067983", 
        'entityType':"operating",
        'sic':"6331",
        'sicDescription':"Fire, Marine & Casualty Insurance",
        'ownerOrg':"02 Finance",
        'insiderTransactionForOwnerExists':1,
        'insiderTransactionForIssuerExists':1,
        'name':"BERKSHIRE HATHAWAY INC",
        'tickers':["BRK-B", "BRK-A"],
        'exchanges':["NYSE", "NYSE"],
        'ein':"470813844",
        'lei':"",
        'description':"",
        'website':"",
        'investorWebsite':"",
        'category':"Large accelerated filer",
        'fiscalYearEnd':"1231",
        'stateOfIncorporation':"DE",
        'stateOfIncorporationDescription':"DE",
        'addresses':{'mailing':{
                'street1':"3555 FARNAM STREET",
                'street2':"",
                'city':"OMAHA",
                'stateOrCountry':"NE",
                'zipCode':"68131",
                'stateOrCountryDescription':"NE",
                'isForeignLocation':"0",
                'foreignStateTerritory':"",
                'country':"",
                'countryCode':""
            },
            'business':{
                'street1':"3555 FARNAM STREET",
                'street2':"",
                'city':"OMAHA",
                'stateOrCountry':"NE",
                'zipCode':"68131",
                'stateOrCountryDescription':"NE",
                'isForeignLocation':"0",
                'foreignStateTerritory':"",
                'country':"",
                'countryCode':""
            }},
        'phone':"4023461400",
        'flags':"",
        'formerNames':[{
            'name':"NBH INC",
            'from':"1998-08-10",
            'to':"1999-01-05"
            }],
        'filings':{'recent':{
            'form':["13F-HR"],
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
                ],
            'acceptanceDateTime':["2023-08-14T20:01:03.000Z"]
            }}
        }
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = json.dumps(mock_response)
    mock_submissions = Submission(**json.loads(mock_api_caller.call.return_value))
    mock_recent = {'recent':{
            'form':["13F-HR"],
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
                ],
            'acceptanceDateTime':["2023-08-14T20:01:03.000Z"]
            }}
    mock_edgar_service.filter_recent.return_value = mock_recent
    mock_submissions.filings.recent = mock_recent
    mock_message_handler.publish = AsyncMock()

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller,
        mock_edgar_service,
        mock_message_handler,
        mock_xml_parser_service,
        mock_html_parser_service
    )

    submissions = await filings_usecase.get_all_submissions(cik="0001067983", headers={'User-Agent': 'test@email.com'}, filing_type=["13F-HR", "13F-HR/A"])

    # Then
    assert submissions == mock_submissions.model_dump()

# get_portfolio 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio(
    mock_api_caller: MagicMock,
    mock_edgar_service: MagicMock,
    mock_message_handler: MagicMock,
    mock_xml_parser_service: MagicMock,
    mock_html_parser_service: MagicMock
) -> None:
    # Given & Mock
    mock_edgar_service.get_portfolio_url.return_value = "https://www.A.com"
    mock_api_caller.call = AsyncMock()
    mock_api_caller.call.return_value = "<infoTable><nameOfIssuer>CHUBB LIMITED</nameOfIssuer><titleOfClass>COM</titleOfClass><cusip>H1467J104</cusip><value>8163932430</value><shrsOrPrnAmt><sshPrnamt>27033784</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt><investmentDiscretion>DFND</investmentDiscretion><otherManager>4,11</otherManager><votingAuthority><Sole>27033784</Sole><Shared>0</Shared><None>0</None></votingAuthority></infoTable>"
    mock_xml_parser_service.xml_to_dict.return_value = {
        "infoTable": [{
            "nameOfIssuer": "ALLY FINL INC", 
            "titleOfClass": "COM", 
            "cusip": "02005N100", 
            "value": "463886547", 
            "shrsOrPrnAmt": {
                "sshPrnamt": "12719675", 
                "sshPrnamtType": "SH"
            }, 
            "investmentDiscretion": "DFND", 
            "otherManager": "4", 
            "votingAuthority": {
                "Sole": "12719675", 
                "Shared": "0", 
                "None": "0"
            }
        }]
    }
    mock_html_parser_service.find_xml.return_value = "FileName"
    mock_message_handler.publish = AsyncMock()

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller, 
        mock_edgar_service,
        mock_message_handler,
        mock_xml_parser_service,
        mock_html_parser_service
        )
    urls = await filings_usecase.get_portfolio(cik="0001067983", headers={'User-Agent': 'test@email.com'}, accession_number="0000950123-25-005701")

    # Then
    assert urls == mock_xml_parser_service.xml_to_dict.return_value

# get_corp_code 단위 테스트
@pytest.mark.anyio
async def test_get_corp_code(
    mock_api_caller: MagicMock,
    mock_dart_service: MagicMock,
    mock_edgar_service: MagicMock,
    mock_message_handler: MagicMock,
    mock_xml_parser_service: MagicMock,
    mock_html_parser_service: MagicMock
) -> None:
    # Given & Mock
    mock_dart_service.get_corp_code_url.return_value = "https://www.A.com"
    mock_api_caller.call_for_file = AsyncMock()
    mock_api_caller.call_for_file.return_value = "Binary Code"
    mock_message_handler.publish_files = AsyncMock()
    mock_message_handler.publish_files.return_value = "file_name"

    # When & Mocking
    filings_usecase = FilingsUsecase(
        mock_api_caller, 
        mock_dart_service,
        mock_edgar_service,
        mock_message_handler,
        mock_xml_parser_service,
        mock_html_parser_service
        )
    file_name = await filings_usecase.get_corp_code()

    # Then
    assert file_name == mock_message_handler.publish_files.return_value