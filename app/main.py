# import ~~~
# from ~ import ~~~
# from ~~ import ~~~
# from ~~~ import ~~~
from fastapi import FastAPI

# from app/~ import ~~~
from api.deps import di_manager
from api.routes.api_routes import ApiRoutes

config_manager = di_manager.get_config_manager()
api_version = config_manager.get_api_version()

app = FastAPI(
    title=config_manager.get_project_name(),
    openapi_url=f"{api_version}/openapi.json"
)

router = ApiRoutes()
app.include_router(router.get_router(), prefix=api_version)

# Kafka 인스턴스 추가
