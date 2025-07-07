from fastapi import Depends, Request

from core.logger import Logger
from core.config import Settings
from core.external_interfaces.kafka_service_impl import KafkaServiceImpl
from core.external_interfaces.parser_service_impl import PaserServiceImpl
from core.external_interfaces.edgar_api_service_impl import EdgarApiServiceImpl

from domain.logger_manager import LoggerManager
from domain.config_manager import ConfigManager
from domain.usecases.services.kafka_service import KafkaService
from domain.usecases.services.parser_service import PaserService
from domain.usecases.services.edgar_api_service import EdgarApiService
from domain.usecases.fillings_usecase import FillingsUsecase

# fastapi는 의존성 부여를 endpoint에서 시작하고, 
# 함수 형태로만 의존성 부여를 하기 때문에 class가 아닌 일반 함수 사용

## Logger
def get_logger_manager() -> LoggerManager:
    return Logger()

## Config
def get_config_manager() -> ConfigManager:
    return Settings()

## Services
def get_paser_service() -> PaserService:
    return PaserServiceImpl()
def get_kafka_service(request: Request) -> KafkaService:
    return request.app.state.kafka_service
def get_edgar_api_service() -> EdgarApiService:
    return EdgarApiServiceImpl()

## Usecases
def get_fillings_usecase(
        kafka_service: KafkaService = Depends(get_kafka_service),
        paser_service: PaserService = Depends(get_paser_service),
        edgar_api_service: EdgarApiService = Depends(get_edgar_api_service)
) -> FillingsUsecase:
    return FillingsUsecase(kafka_service, paser_service, edgar_api_service)

## Connection
def get_kafka_connection() -> KafkaService:
    return KafkaServiceImpl(get_config_manager())