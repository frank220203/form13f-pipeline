import pytest
from unittest.mock import MagicMock, AsyncMock
from domain.usecases.pipeline_usecase import PipelineUsecase

# get_all_tickers 단위 테스트
@pytest.mark.anyio
async def test_load_tickers(
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    mock_ticker_repository.add_data = AsyncMock()
    mock_ticker_repository.add_data.return_value = 1

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_ticker_repository, 
        mock_portfolio_repository,
        mock_submission_repository
        )

    load_success = await pipeline_usecase.load_tickers(data="")

    # Then
    assert load_success == mock_ticker_repository.add_data.return_value

@pytest.mark.anyio
async def test_load_submissions(
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    mock_submission_repository.add_data = AsyncMock()
    mock_submission_repository.add_data.return_value = 1

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_ticker_repository,
        mock_portfolio_repository,
        mock_submission_repository
        )

    load_success = await pipeline_usecase.load_submissions(data="")

    # Then
    assert load_success == mock_submission_repository.add_data.return_value

@pytest.mark.anyio
async def test_load_portfolios(
    mock_ticker_repository: MagicMock, 
    mock_portfolio_repository: MagicMock,
    mock_submission_repository: MagicMock
    ) -> None:
    # Given & Mock
    mock_portfolio_repository.add_data = AsyncMock()
    mock_portfolio_repository.add_data.return_value = 1

    # When & Mocking
    pipeline_usecase = PipelineUsecase(
        mock_ticker_repository, 
        mock_portfolio_repository,
        mock_submission_repository
        )
    
    load_success = await pipeline_usecase.load_portfolios(data="")

    # Then
    assert load_success == mock_portfolio_repository.add_data.return_value
