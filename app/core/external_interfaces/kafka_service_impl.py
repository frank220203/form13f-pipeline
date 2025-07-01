import json
from aiokafka import AIOKafkaProducer
from core.config import Settings
from domain.usecases.services.kafka_service import KafkaService

class KafkaServiceImpl(KafkaService):

    # __settings = Settings()
    # __producer = AIOKafkaProducer(
    #     bootstrap_servers=__settings.KAFKA_BROKER_IP.split(","),
    #     value_serializer=lambda v: json.dumps(v).encode('utf-8')
    #     )

    __producer: AIOKafkaProducer

    def __init__(self, settings: Settings):
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=settings.get_kafka_broker_ip()
        )

    async def publish(self, topic: str, msg:str) -> None:
        
        # 카프카 연결은 컨트롤러가 아닌 브로커에 연결 하고, 여러 브로커 중에 임의로 하나만 연결해도 됨.
        print(msg)
        await self.__producer.send(topic, json.dumps(msg).encode('utf-8'))

    async def start(self) -> None:
        await self.__producer.start()

    async def stop(self) -> None:
        await self.__producer.stop()