import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from domain.models.crosswalk import Crosswalk
from domain.models.portfolios.portfolio import Portfolio
from domain.usecases.pipeline_usecase import PipelineUsecase

# load_tickers 단위 테스트
@pytest.mark.anyio
async def test_load_tickers(
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_crosswalk_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    mock_ticker_repository.add_data = AsyncMock()
    mock_ticker_repository.add_data.return_value = {
        'cik' : '1045810',
        'name' : 'NVIDIA CORP',
        'ticker' : 'NVDA',
        'exchange' : 'Nasdaq'
    }
    ticker_list = []
    ticker_list.append(mock_ticker_repository.add_data.return_value)

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_ticker_repository, 
        mock_portfolio_repository,
        mock_crosswalk_repository,
        mock_submission_repository
        )

    load_success = await pipeline_usecase.load_tickers(data={
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
    })
    print(load_success)

    # Then
    assert load_success == ticker_list

# load_submissions 단위 테스트
@pytest.mark.anyio
async def test_load_submissions(
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_crosswalk_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    msg = {
        'cik':'0001067983', 
        'entityType':'operating',
        'sic':'6331',
        'sicDescription':'Fire, Marine & Casualty Insurance',
        'ownerOrg':'02 Finance',
        'insiderTransactionForOwnerExists':1,
        'insiderTransactionForIssuerExists':1,
        'name':'BERKSHIRE HATHAWAY INC',
        'tickers':['BRK-B', 'BRK-A'],
        'exchanges':['NYSE', 'NYSE'],
        'ein':'470813844',
        'lei':'',
        'description':'',
        'website':'',
        'investorWebsite':'',
        'category':'Large accelerated filer',
        'fiscalYearEnd':'1231',
        'stateOfIncorporation':'DE',
        'stateOfIncorporationDescription':'DE',
        'addresses':{'mailing':{
                'street1':'3555 FARNAM STREET',
                'street2':'',
                'city':'OMAHA',
                'stateOrCountry':'NE',
                'zipCode':'68131',
                'stateOrCountryDescription':'NE',
                'isForeignLocation':'0',
                'foreignStateTerritory':'',
                'country':'',
                'countryCode':''
            },
            'business':{
                'street1':'3555 FARNAM STREET',
                'street2':'',
                'city':'OMAHA',
                'stateOrCountry':'NE',
                'zipCode':'68131',
                'stateOrCountryDescription':'NE',
                'isForeignLocation':'0',
                'foreignStateTerritory':'',
                'country':'',
                'countryCode':''
            }},
        'phone':'4023461400',
        'flags':'',
        'formerNames':[{
            'name':'NBH INC',
            'from':'1998-08-10',
            'to':'1999-01-05'
            }],
        'filings':{'recent':{
            'form':['13F-HR'],
            'accessionNumber':[
                '0000950123-25-00570', 
                '0000950170-25-102306', 
                '0000950170-25-102303'
                ],
            'filingDate':[
                '2025-08-04',
                '2025-08-04',
                '2025-08-04'
                ],
            'reportDate':[
                '2025-07-31',
                '2025-07-31',
                '2025-07-31'
                ],
            'acceptanceDateTime':['2023-08-14T20:01:03.000Z']
            }}
        }
    mock_submission_repository.add_data = AsyncMock()
    mock_submission_repository.add_data.return_value = msg

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_ticker_repository,
        mock_portfolio_repository,
        mock_crosswalk_repository,
        mock_submission_repository
        )
    
    load_success = await pipeline_usecase.load_submissions(data=json.dumps(msg))

    # Then
    assert load_success == mock_submission_repository.add_data.return_value

# load_portfolios 단위 테스트
@pytest.mark.anyio
async def test_load_portfolios(
    mock_prompt_service: MagicMock,
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_crosswalk_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    msg = {
        'header_data': {
            'submission_type' : '13F-HR',
            'filer_info' : {
                'live_test_flag' : 'LIVE',
                'flags' : None,
                'filer' : {
                    'credentials' : {
                        'cik' : '0001067983',
                        'ccc' : 'XXXXXXX'
                    }
                },
                'period_of_report' : '06-30-2025'
            }
        },
        'form_data' : {
            'cover_page' : {
                'report_calendar_or_quartor' : '06-30-2025',
                'is_amendment' : 'false',
                'filing_manager' : {
                    'name' : 'Berkshire Hathaway Inc',
                    'address' : {
                        'ns1_street1' : '3555 Farnam Street',
                        'ns1_city' : 'Omaha',
                        'ns1_state_or_country' : 'NE',
                        'ns1_zip_code' : '68131'
                    },
                },
                'report_type' : '13F HOLDINGS REPORT',
                'form13_f_file_number' : '028-04545',
                'provide_info_for_instruction5' : 'N'
            },
            'signature_block' : {
                'name' : "Marc D. Hamburg",
                'title' : 'Senior Vice President',
                'phone' : '402-346-1400',
                'signature' : 'Marc D. Hamburg',
                'city' : 'Omaha',
                'state_or_country' : 'NE',
                'signature_date' : '08-14-2025'
            },
            'summary_page' : {
                'other_included_managers_count' : '14',
                'table_entry_total' : '114',
                'table_value_total' : '257521776925',
                'is_confidential_omitted' : 'false',
                'other_manager2_info' : {
                    'other_manager2' : [{
                        'sequence_number' : '1',
                        'other_manager' : {
                            'form13_f_file_number' : '28-2226',
                            'name' : 'Berkshire Hathaway Homestate Insurance Co.'
                        }
                    }]
                }
            }
        },
        'issuers' : [{
            'name_of_issuer' : 'ALLY FINL INC',
            'title_of_class' : 'COM',
            'cusip' : '02005N100',
            'value' : '495431341',
            'shrs_or_prn_amt' : {
                'ssh_prnamt' : '12719675'
            },
            'investment_discretion' : 'DFND',
            'other_manager' : '4',
            'voting_authority' : {
                'sole' : '12719675'
            }
        }],
        'ext_date' : '2025-08-29'
    }
    mock_portfolio = json.dumps(msg)
    mock_portfolio_repository.add_data = AsyncMock()
    mock_portfolio_repository.add_data.return_value = Portfolio(**json.loads(mock_portfolio))

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_prompt_service,
        mock_ticker_repository, 
        mock_portfolio_repository,
        mock_crosswalk_repository,
        mock_submission_repository
        )
    
    load_success = await pipeline_usecase.load_portfolios(data=mock_portfolio)

    # Then
    assert load_success == mock_portfolio_repository.add_data.return_value

# load_crosswalks 단위 테스트
@pytest.mark.anyio
async def test_load_crosswalks(
    mock_prompt_service: MagicMock,
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_crosswalk_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    portfolio = {
        'header_data': {
            'submission_type' : '13F-HR',
            'filer_info' : {
                'live_test_flag' : 'LIVE',
                'flags' : None,
                'filer' : {
                    'credentials' : {
                        'cik' : '0001067983',
                        'ccc' : 'XXXXXXX'
                    }
                },
                'period_of_report' : '06-30-2025'
            }
        },
        'form_data' : {
            'cover_page' : {
                'report_calendar_or_quartor' : '06-30-2025',
                'is_amendment' : 'false',
                'filing_manager' : {
                    'name' : 'Berkshire Hathaway Inc',
                    'address' : {
                        'ns1_street1' : '3555 Farnam Street',
                        'ns1_city' : 'Omaha',
                        'ns1_state_or_country' : 'NE',
                        'ns1_zip_code' : '68131'
                    },
                },
                'report_type' : '13F HOLDINGS REPORT',
                'form13_f_file_number' : '028-04545',
                'provide_info_for_instruction5' : 'N'
            },
            'signature_block' : {
                'name' : "Marc D. Hamburg",
                'title' : 'Senior Vice President',
                'phone' : '402-346-1400',
                'signature' : 'Marc D. Hamburg',
                'city' : 'Omaha',
                'state_or_country' : 'NE',
                'signature_date' : '08-14-2025'
            },
            'summary_page' : {
                'other_included_managers_count' : '14',
                'table_entry_total' : '114',
                'table_value_total' : '257521776925',
                'is_confidential_omitted' : 'false',
                'other_manager2_info' : {
                    'other_manager2' : [{
                        'sequence_number' : '1',
                        'other_manager' : {
                            'form13_f_file_number' : '28-2226',
                            'name' : 'Berkshire Hathaway Homestate Insurance Co.'
                        }
                    }]
                }
            }
        },
        'issuers' : [{
            'name_of_issuer' : 'ALLY FINL INC',
            'title_of_class' : 'COM',
            'cusip' : '02005N100',
            'value' : '495431341',
            'shrs_or_prn_amt' : {
                'ssh_prnamt' : '12719675'
            },
            'investment_discretion' : 'DFND',
            'other_manager' : '4',
            'voting_authority' : {
                'sole' : '12719675'
            }
        }],
        'ext_date' : '2025-08-29'
    }
    mock_portfolio = Portfolio(**portfolio)
    mock_portfolio_repository.get_portfolio_by_cik = AsyncMock()
    mock_portfolio_repository.get_portfolio_by_cik.return_value = mock_portfolio
    mock_portfolio_repository.get_distinct_issuers = AsyncMock()
    mock_portfolio_repository.get_distinct_issuers.return_value = ["02005N100"]
    mock_crosswalk_repository.get_crosswalk_by_sin = AsyncMock()
    mock_crosswalk_repository.get_crosswalk_by_sin.return_value = None
    mock_prompt_service.get_naics = AsyncMock()
    mock_prompt_service.get_naics.return_value = ["334123"]
    mock_crosswalk = Crosswalk(sin=mock_portfolio_repository.get_distinct_issuers.return_value[0], naisc=mock_prompt_service.get_naics.return_value[0])
    mock_crosswalk_repository.add_data = AsyncMock()
    mock_crosswalk_repository.add_data.return_value = mock_crosswalk

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_prompt_service,
        mock_ticker_repository, 
        mock_portfolio_repository,
        mock_crosswalk_repository,
        mock_submission_repository
        )
    load_success = await pipeline_usecase.load_crosswalks(cik="0001067983")

    # Then
    assert load_success == mock_crosswalk_repository.add_data.return_value