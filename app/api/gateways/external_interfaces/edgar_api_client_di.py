from fastapi import Depends
from core.external_interfaces.edgar_api_client_impl import EdgarApiClientImpl
from api.gateways.external_interfaces.edgar_api_client import EdgarApiClient

class EdgarApiClientDi():

    __client: EdgarApiClient

    def __init__(self, client: EdgarApiClient = Depends(EdgarApiClientImpl)):
        self.__client = client

    def get_edgar_api_client(self) -> EdgarApiClient:
        return self.__client