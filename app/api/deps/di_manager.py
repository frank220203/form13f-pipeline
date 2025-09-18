from fastapi import Depends, Request

from api.deps import da_manager

from core.logger import Logger
from core.config import Settings

from core.external_interfaces.edgar_service_impl import EdgarServiceImpl

from domain.logger_manager import LoggerManager
from domain.config_manager import ConfigManager

from domain.usecases.filings_usecase import FilingsUsecase

from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.dart_service import DartService
from domain.usecases.services.edgar_service import EdgarService
from domain.usecases.services.message_handler import MessageHandler
from domain.usecases.services.xml_parser_service import XmlPaserService
from domain.usecases.services.html_parser_service import HtmlPaserService

# fastapi는 의존성 부여를 endpoint에서 시작하고, 
# 함수 형태로만 의존성 부여를 하기 때문에 class가 아닌 일반 함수 사용

## Logger
def get_logger_manager() -> LoggerManager:
    return Logger()

## Config
def get_config_manager() -> ConfigManager:
    return Settings()

## Services
def get_kafka_service(request: Request) -> MessageHandler:
    return request.app.state.kafka_service
def get_edgar_service(settings: ConfigManager = Depends(da_manager.get_config_manager)) -> EdgarService:
    return EdgarServiceImpl(settings)

## Usecases
def get_filings_usecase(
        api_caller: ApiCaller = Depends(da_manager.get_api_caller),
        dart_service: DartService = Depends(da_manager.get_dart_service),
        edgar_service: EdgarService = Depends(get_edgar_service),
        message_handler: MessageHandler = Depends(get_kafka_service),
        xml_paser_service: XmlPaserService = Depends(da_manager.get_xml_paser_service),
        html_paser_service: HtmlPaserService = Depends(da_manager.get_html_paser_service)
) -> FilingsUsecase:
    return FilingsUsecase(
        api_caller, 
        dart_service,
        edgar_service, 
        message_handler, 
        xml_paser_service, 
        html_paser_service
        )