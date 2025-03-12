import json

from kafka import KafkaProducer
from domain.usecases.services.kafka_service import KafkaService

class KafkaServiceImpl(KafkaService):

    __producer = KafkaProducer(
        bootstrap_servers=['localhost:29092', 'localhost:39092', 'localhost:49092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_message(self, msg:str) -> None:
        
        # 카프카 연결은 컨트롤러가 아닌 브로커에 연결 하고, 여러 브로커 중에 임의로 하나만 연결해도 됨.
        self.__producer.send('portfolio', key=b'1', value=msg)
        self.__producer.flush()
        self.__producer.close()

    def consume_messages(self):
        pass