from abc import ABC, abstractmethod

class MessageHandler(ABC):
    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, msg: str) -> None:
        pass

    @abstractmethod
    async def publish_files(self, topic: str, key: bytes, value: bytes) -> str:
        pass

    @abstractmethod
    async def read(self) -> str:
        pass