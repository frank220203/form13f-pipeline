import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from core.config import Settings

from domain.usecases.pipeline_usecase import PipelineUsecase
from domain.usecases.services.message_handler import MessageHandler

class KafkaServiceImpl(MessageHandler):

    __consumer: AIOKafkaConsumer
    __producer: AIOKafkaProducer
    __pipeline_usecase: PipelineUsecase

    # 카프카 연결은 컨트롤러가 아닌 브로커에 연결 하고, 여러 브로커 중에 임의로 하나만 연결해도 됨.
    def __init__(self, settings: Settings):
        self.__producer = AIOKafkaProducer(bootstrap_servers=settings.get_kafka_broker_ip())
        self.__consumer = AIOKafkaConsumer(
            settings.get_kafka_topic(), 
            bootstrap_servers=settings.get_kafka_broker_ip(), 
            group_id=settings.get_kafka_group_pf(), 
            auto_offset_reset="latest"
        )
        self.__pipeline_usecase = PipelineUsecase()

    async def stop(self) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()

    async def start(self) -> None:
        await self.__producer.start()
        await self.__consumer.start()

    async def publish(self, topic: str, msg:str) -> None:
        # 중복 메시지 처리 로직 필요
        await self.__producer.send(topic, json.dumps(msg).encode('utf-8'))

    async def read(self) -> None:
        async for msg in self.__consumer:
            msg_to_str = msg.value.decode("utf-8")
            self.__pipeline_usecase.load_data(msg_to_str)