from abc import ABC, abstractmethod

class KafkaConsumer(ABC):
    @abstractmethod
    def consume_portfolio(self, msg: str) -> None:
        pass