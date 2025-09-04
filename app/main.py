# import ~~~
import asyncio
# from ~ import ~~~
# from ~~ import ~~~
# from ~~~ import ~~~
from fastapi import FastAPI
from contextlib import asynccontextmanager

# from app/~ import ~~~
from api.deps import da_manager
from api.routes.api_routes import ApiRoutes
from core.middlewares.logging_middleware import LoggingMiddleware

# 로거
logger = da_manager.get_logger_manager().get_logger()

# 환경설정
config_manager = da_manager.get_config_manager()
api_version = config_manager.get_api_version()

# App 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application lifespan startup initiated.")
    # MongoDB 실행
    db_connector = da_manager.get_db_manager()
    await db_connector.init_db()
    logger.info("MongoDB is connected")
    # Kafka 실행
    kafka_connector = da_manager.get_kafka_connection()
    await kafka_connector.start()
    app.state.kafka_service = kafka_connector
    logger.info("Kafka service stored in app.state.")
    # 컨슈머 백그라운드 실행
    asyncio.create_task(app.state.kafka_service.read())
    logger.info("Kafka consumer is working")

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