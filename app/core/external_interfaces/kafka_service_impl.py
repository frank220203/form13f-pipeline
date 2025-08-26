import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from domain.config_manager import ConfigManager
from domain.logger_manager import LoggerManager
from domain.usecases.pipeline_usecase import PipelineUsecase
from domain.usecases.services.message_handler import MessageHandler

class KafkaServiceImpl(MessageHandler):

    __logger: LoggerManager
    __consumer: AIOKafkaConsumer
    __producer: AIOKafkaProducer
    __pipeline_usecase: PipelineUsecase

    # 카프카 연결은 컨트롤러가 아닌 브로커에 연결 하고, 여러 브로커 중에 임의로 하나만 연결해도 됨.
    def __init__(self, settings: ConfigManager, logger: LoggerManager, pipeline_usecase: PipelineUsecase):
        self.__logger = logger.get_logger()
        self.__producer = AIOKafkaProducer(bootstrap_servers=settings.get_kafka_broker_ip())
        self.__consumer = AIOKafkaConsumer(
            *settings.get_kafka_topic().split(","), 
            bootstrap_servers=settings.get_kafka_broker_ip(), 
            group_id=settings.get_kafka_group_pf(), 
            # auto_offset_reset="latest"
        )
        self.__pipeline_usecase = pipeline_usecase

    async def stop(self) -> None:
        await self.__producer.stop()
        await self.__consumer.stop()

    async def start(self) -> None:
        await self.__producer.start()
        await self.__consumer.start()

    async def publish(self, topic: str, msg:str) -> None:
        # add_callback 넣으면 pytest가 불가
        # await self.__producer.send(topic, json.dumps(msg).encode('utf-8')).add_callback(self.__on_success).add_errback(self.__on_error)
        # 중복 메시지 처리 로직 필요
        await self.__producer.send(topic, json.dumps(msg).encode('utf-8'))

    async def read(self) -> str:
        # index를 맨 앞으로 변경
        await self.__consumer.seek_to_beginning()
        async for msg in self.__consumer:
            msg_to_str = msg.value.decode("utf-8")
            if msg.topic == 'ticker':
                result = await self.__pipeline_usecase.load_tickers(msg_to_str)
            elif msg.topic == 'submission':
                result = await self.__pipeline_usecase.load_submissions(msg_to_str)
            elif msg.topic == 'portfolio':
                result = await self.__pipeline_usecase.load_portfolios(msg_to_str)
            # 단건 테스트용 break
            break
        log_msg = str(result)[:300]
        if len(log_msg) > 100:
            self.__logger.info(f"Kafka consumed message : {log_msg[:100]}")
        else:
            self.__logger.info(f"Kafka consumed message : {log_msg}")

        return "Kafka consumed message"
                

    def __on_success(self, record_metadata) -> None:
        self.__logger.info(f"Message successfully sent to {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")

    def __on_error(self, excp) -> None:
        self.__logger.info(f"Failed to send message: {excp}")