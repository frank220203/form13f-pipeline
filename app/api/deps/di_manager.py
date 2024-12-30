from fastapi import Depends

from core.external_interfaces.parser_service_impl import PaserServiceImpl
from core.external_interfaces.edgar_api_service_impl import EdgarApiServiceImpl

from domain.usecases.services.parser_service import PaserService
from domain.usecases.services.edgar_api_service import EdgarApiService
from domain.usecases.fillings_usecase import FillingsUsecase

# fastapi는 의존성 부여를 endpoint에서 시작하고, 
# 함수 형태로만 의존성 부여를 하기 때문에 class가 아닌 일반 함수 사용

## Services
def get_paser_service() -> PaserService:
    return PaserServiceImpl()
def get_edgar_api_service() -> EdgarApiService:
    return EdgarApiServiceImpl()

## Usecases
def get_fillings_usecase(
        paser_service: PaserService = Depends(get_paser_service),
        edgar_api_service: EdgarApiService = Depends(get_edgar_api_service)
) -> FillingsUsecase:
    return FillingsUsecase(paser_service, edgar_api_service)