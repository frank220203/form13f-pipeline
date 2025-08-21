import json
from typing import List

from domain.models.ticker import Ticker
from domain.usecases.repositories.ticker_repository import TickerRepository

class PipelineUsecase:

    __ticker_repository: TickerRepository

    def __init__(self, ticker_repository: TickerRepository):
        self.__ticker_repository = ticker_repository

    async def load_tickers(self, data: str) -> List[dict]:
        
        try:
            while isinstance(data, str):
                data = json.loads(data)
        except Exception as e:
            raise e     
        fields = data['fields']
        tickers = data['data']
        ticker_list = []
        for ticker in tickers:
            ticker_dict = dict(zip(fields, ticker))
            ticker_list.append(await self.__ticker_repository.add_data(Ticker(**ticker_dict)))

        return ticker_list