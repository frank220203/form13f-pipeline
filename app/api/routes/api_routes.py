from fastapi import APIRouter
from api.controllers.filings_controller import FilingsController

class ApiRoutes:
    
    __router: APIRouter
    __filingsController: FilingsController
    
    def __init__(self):
        self.__router = APIRouter()
        self.__filingsController = FilingsController()
        self.__router.include_router(self.__filingsController.get_router())
    
    def get_router(self):
        return self.__router