from core.logger import Logger
from core.config import Settings

from core.external_interfaces.httpx_client import HttpxClient
from core.external_interfaces.gemini_prompt import GeminiPrompt
from core.external_interfaces.dart_service_impl import DartServiceImpl
from core.external_interfaces.kafka_service_impl import KafkaServiceImpl
from core.external_interfaces.xml_parser_service_impl import XmlPaserServiceImpl
from core.external_interfaces.html_parser_service_impl import HtmlPaserServiceImpl

from core.repositories.beanie_repository import BeanieRepository
from core.repositories.ticker_repository_impl import TickerRepositoryImpl
from core.repositories.portfolio_repository_impl import PortfolioRepositoryImpl
from core.repositories.crosswalk_repository_impl import CrosswalkRepositoryImpl
from core.repositories.submission_repository_impl import SubmissionRepositoryImpl

from domain.db_manager import DbManager
from domain.config_manager import ConfigManager
from domain.logger_manager import LoggerManager

from domain.usecases.pipeline_usecase import PipelineUsecase

from domain.usecases.services.api_caller import ApiCaller
from domain.usecases.services.dart_service import DartService
from domain.usecases.services.prompt_service import PromptService
from domain.usecases.services.message_handler import MessageHandler
from domain.usecases.services.xml_parser_service import XmlPaserService
from domain.usecases.services.html_parser_service import HtmlPaserService

from domain.usecases.repositories.ticker_repository import TickerRepository
from domain.usecases.repositories.portfolio_repository import PortfolioRepository
from domain.usecases.repositories.crosswalk_repository import CrosswalkRepository
from domain.usecases.repositories.submission_repository import SubmissionRepository

# fastapi에서 의존성 주입은 어댑터 계층에 도메인 계층을 주입할 때만 사용
# 그 외에는 의존성 조립을 통해 도메인 계층의 서비스를 전달
# 엔드포인트를 통해서만 의존성을 주입하는 fastapi이기에 엔드포인트를 통하지 않는 서비스들은 Depends를 못 쓰고, 직접 명시해 줘야한다.
## Logger
def get_logger_manager() -> LoggerManager:
    return Logger()

## Config
def get_config_manager() -> ConfigManager:
    return Settings()

## DB Session
def get_db_manager() -> DbManager:
    return BeanieRepository(settings=get_config_manager())

## Usecases
def get_pipeline_usecase() -> PipelineUsecase:
    return PipelineUsecase(
        prompt_service = get_prompt_service(),
        ticker_repository = get_ticker_repository(), 
        portfolio_repository = get_portfolio_repository(), 
        crosswalk_repository = get_crosswalk_repository(),
        submission_repository = get_submission_repository()
        )

## Services
def get_api_caller() -> ApiCaller:
    return HttpxClient()
def get_dart_service() -> DartService:
    return DartServiceImpl(get_config_manager())
def get_prompt_service() -> PromptService:
    return GeminiPrompt(get_config_manager())
def get_xml_paser_service() -> XmlPaserService:
    return XmlPaserServiceImpl()
def get_html_paser_service() -> HtmlPaserService:
    return HtmlPaserServiceImpl()

## Repositories
def get_ticker_repository() -> TickerRepository:
    return TickerRepositoryImpl()
def get_portfolio_repository() -> PortfolioRepository:
    return PortfolioRepositoryImpl()
def get_crosswalk_repository() -> CrosswalkRepository:
    return CrosswalkRepositoryImpl()
def get_submission_repository() -> SubmissionRepository:
    return SubmissionRepositoryImpl()

## Connection
def get_kafka_connection() -> MessageHandler:
    return KafkaServiceImpl(
        settings = get_config_manager(), 
        logger = get_logger_manager(), 
        pipeline_usecase = get_pipeline_usecase()
        )