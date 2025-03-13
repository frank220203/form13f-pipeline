from abc import ABC, abstractmethod

class KafkaService(ABC):
    @abstractmethod
    def produce_portfolio(self, msg: str) -> None:
        pass

    @abstractmethod
    def consume_messages(self) -> dict:
        pass