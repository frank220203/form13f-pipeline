# import ~~~
# from ~ import ~~~
# from ~~ import ~~~
# from ~~~ import ~~~
from fastapi import FastAPI
from contextlib import asynccontextmanager

# from app/~ import ~~~
from api.deps import di_manager
from api.routes.api_routes import ApiRoutes
from core.middlewares.logging_middleware import LoggingMiddleware

# 로거
logger = di_manager.get_logger_manager().get_logger()

# 환경설정
config_manager = di_manager.get_config_manager()
api_version = config_manager.get_api_version()

# App 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application lifespan startup initiated.")
    # Kafka 실행
    kafka_connector = di_manager.get_kafka_connection()
    await kafka_connector.start()
    # await kafka_connector.read()
    logger.info("Kafka consumer is working")
    app.state.kafka_service = kafka_connector
    logger.info("Kafka service stored in app.state.")

    yield

    # Kafka 종료
    logger.info("Application lifespan shutdown initiated.")
    if hasattr(app.state, 'kafka_service') and app.state.kafka_service:
        await app.state.kafka_service.stop()
        logger.info("Kafka service stopped during shutdown.")

# FastAPI 실행
app = FastAPI(
    title=config_manager.get_project_name(),
    openapi_url=f"{api_version}/openapi.json",
    lifespan=lifespan
)

# 엔드포인트 추가
router = ApiRoutes()
app.include_router(router.get_router(), prefix=api_version)

# 로깅 필터 추가
app.add_middleware(LoggingMiddleware)