from abc import ABC, abstractmethod

class KafkaService(ABC):
    @abstractmethod
    async def publish(self, topic:str, msg: str) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass