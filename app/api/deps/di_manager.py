from fastapi import Depends, Request

from core.logger import Logger
from core.config import Settings
from core.repositories.beanie_repository import BeanieRepository
from core.external_interfaces.httpx_client import HttpxClient
from core.external_interfaces.edgar_service_impl import EdgarServiceImpl
from core.external_interfaces.kafka_service_impl import KafkaServiceImpl
from core.external_interfaces.parser_service_impl import PaserServiceImpl

from domain.db_manager import DbManager
from domain.logger_manager import LoggerManager
from domain.config_manager import ConfigManager
from domain.usecases.filings_usecase import FilingsUsecase
from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.edgar_service import EdgarService
from domain.usecases.services.parser_service import PaserService
from domain.usecases.services.message_handler import MessageHandler

# fastapi는 의존성 부여를 endpoint에서 시작하고, 
# 함수 형태로만 의존성 부여를 하기 때문에 class가 아닌 일반 함수 사용

## Logger
def get_logger_manager() -> LoggerManager:
    return Logger()

## Config
def get_config_manager() -> ConfigManager:
    return Settings()

## DB Session
def get_db_manager() -> DbManager:
    return BeanieRepository(get_config_manager())

## Services
def get_api_caller() -> ApiCaller:
    return HttpxClient()
def get_paser_service() -> PaserService:
    return PaserServiceImpl()
def get_kafka_service(request: Request) -> MessageHandler:
    return request.app.state.kafka_service
def get_edgar_service() -> EdgarService:
    return EdgarServiceImpl(get_config_manager())

## Usecases
def get_filings_usecase(
        api_caller: ApiCaller = Depends(get_api_caller),
        edgar_service: EdgarService = Depends(get_edgar_service),
        paser_service: PaserService = Depends(get_paser_service),
        message_handler: MessageHandler = Depends(get_kafka_service),
) -> FilingsUsecase:
    return FilingsUsecase(api_caller, edgar_service, paser_service, message_handler)

## Connection
def get_kafka_connection() -> MessageHandler:
    return KafkaServiceImpl(get_config_manager())