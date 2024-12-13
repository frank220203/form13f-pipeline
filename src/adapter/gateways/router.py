from fastapi import APIRouter, Depends
from infrastructure.external_interfaces.edgar_api_client_impl import EdgarApiClientImpl

class Router:
    def __init__(self):
        self.edgar_api_client = EdgarApiClientImpl()
        self.router = APIRouter()

        self.router.add_api_route("/apitest", self.get_13f_data, methods=["GET"])
    
    def get_13f_data(self) :
        return self.edgar_api_client.get_13f_data()
    
    def get_router(self):
        return self.router
