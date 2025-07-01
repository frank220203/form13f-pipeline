# import ~~~
# from ~ import ~~~
# from ~~ import ~~~
# from ~~~ import ~~~
from fastapi import FastAPI
from contextlib import asynccontextmanager

# from app/~ import ~~~
from api.deps import di_manager
from api.routes.api_routes import ApiRoutes

# 환경설정
config_manager = di_manager.get_config_manager()
api_version = config_manager.get_api_version()

# 엔드포인트 추가
router = ApiRoutes()

# App 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application lifespan startup initiated.")
    # Kafka 실행
    kafka_service = di_manager.get_kafka_connection()
    await kafka_service.start()
    app.state.kafka_service = kafka_service
    print("Kafka producer stored in app.state.")

    yield

    # Kafka 종료
    print("Application lifespan shutdown initiated.")
    if hasattr(app.state, 'kafka_service') and app.state.kafka_service:
        await app.state.kafka_service.stop()
        print("Kafka producer stopped during shutdown.")

# FastAPI 실행
app = FastAPI(
    title=config_manager.get_project_name(),
    openapi_url=f"{api_version}/openapi.json",
    lifespan=lifespan
)
app.include_router(router.get_router(), prefix=api_version)