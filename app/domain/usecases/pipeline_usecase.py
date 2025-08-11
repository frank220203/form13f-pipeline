from domain.usecases.repositories.ticker_repository import TickerRepository

class PipelineUsecase:

    __ticker_repository: TickerRepository

    def __init__(self, ticker_repository: TickerRepository):
        self.__ticker_repository = ticker_repository

    async def load_tickers(self, data: str) -> dict:
        print(f"load data : {data}")
        tickers = await self.__ticker_repository.add_data(data)
        return tickers