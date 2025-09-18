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
        # async_client: AsyncClient,
        client: TestClient,
        mock_filings_usecase: MagicMock
) -> None:
    #Mock
    mock_filings_usecase.get_all_tickers = AsyncMock()
    mock_filings_usecase.get_all_tickers.return_value = {
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
    
    # Mocking // 의존성 주입을 안 할 경우 실제 API를 타게 됨 (통합테스트 가능)
    app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    # TestClient 자체는 동기적으로 작동하기 때문에 await 쓰지 않음
    # response = await client.get(f"{api_version}/filings/tickers?email=test@email.com")
    response = client.get(f"{api_version}/filings/tickers?email=test@email.com")

    # Then
    assert response.status_code == 200
    assert response.json() == {'tickers':mock_filings_usecase.get_all_tickers.return_value}

@pytest.mark.anyio
async def test_get_all_submissions(
    client: TestClient,
    mock_filings_usecase: MagicMock
) -> None:
    # Mock
    mock_filings_usecase.get_all_submissions = AsyncMock()
    mock_filings_usecase.get_all_submissions.return_value = {
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

    # Mocking
    app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    response = client.get(f"{api_version}/filings/submissions?cik=0001067983&email=test@email.com&filing_type=13F-HR&filing_type=13F-HR/A")
    
    # Then 
    assert response.status_code == 200
    assert response.json() == {'submissions': mock_filings_usecase.get_all_submissions.return_value}

# get_portfolio 단위 테스트
@pytest.mark.anyio
async def test_get_portfolio(
    client: TestClient,
    mock_filings_usecase: MagicMock
) -> None:
    # Mock
    mock_filings_usecase.get_portfolio = AsyncMock()
    mock_filings_usecase.get_portfolio.return_value = {
        'headerData': {
            'submissionType': "13F-HR", 
            'filerInfo': {
                'liveTestFlag': "LIVE", 
                'flags': {
                    'confirmingCopyFlag': 'false', 
                    'returnCopyFlag': 'true', 
                    'overrideInternetFlag': 'false'
                }, 
                'filer': {'credentials': {
                        'cik': "0001067983", 
                        'ccc': "XXXXXXXX"
                    }}, 
                'periodOfReport': "03-31-2025"
            }
        },
        'formData': {
            'filingManager': {
                'name': "Berkshire Hathaway Inc", 
                'address': {
                    'ns1:street1': "3555 Farnam Street", 
                    'ns1:city': "Omaha", 
                    'ns1:stateOrCountry': "NE", 
                    'ns1:zipCode': "68131"
                }
            },
            'summaryPage': {
                'otherIncludedManagersCount': "14", 
                'tableEntryTotal': "110", 
                'tableValueTotal': "258701144516", 
                'isConfidentialOmitted': 'true', 
                'otherManagers2Info': {'otherManager2': [{
                    'sequenceNumber': "1", 
                    'otherManager': {
                        'form13FFileNumber': "28-2226", 
                        'name': "Berkshire Hathaway Homestate Insurance Co."
                    }
                }]}
            },
        },
        'infoTable': [{
            'nameOfIssuer': "ALLY FINL INC", 
            'titleOfClass': "COM", 
            'cusip': "02005N100", 
            'value': "463886547", 
            'shrsOrPrnAmt': {
                'sshPrnamt': "12719675", 
                'sshPrnamtType': "SH"
            }, 
            'investmentDiscretion': "DFND", 
            'otherManager': "4", 
            'votingAuthority': {
                'Sole': "12719675", 
                'Shared': "0", 
                'None': "0"
            }
        }]
    }

    # Mocking
    app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    response = client.get(f"{api_version}/filings/portfolio?email=sample@email.com&cik=0001067983&accession_number=0000950123-25-008343")

    # Then
    assert response.status_code == 200
    assert response.json() == {'porfolio': mock_filings_usecase.get_portfolio.return_value}

# get_corp_code 단위 테스트
@pytest.mark.anyio
async def test_get_corp_code(
    client: TestClient,
    mock_filings_usecase: MagicMock
) -> None:
    # Mock
    mock_filings_usecase.get_corp_code = AsyncMock()
    mock_filings_usecase.get_corp_code.return_value = "sample.zip"

    # Mocking
    # app.dependency_overrides[get_filings_usecase] = lambda: mock_filings_usecase

    # When
    response = client.get(f"{api_version}/filings/corpCode")

    # Then
    assert response.status_code == 200
    assert response.json() == {'fileName': mock_filings_usecase.get_corp_code.return_value}