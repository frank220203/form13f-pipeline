from fastapi import APIRouter
from api.controllers.fillings_controller import FillingsController

class ApiRoutes:
    
    __router: APIRouter
    __fillingsController: FillingsController
    
    def __init__(self):
        self.__router = APIRouter()
        self.__fillingsController = FillingsController()
        self.__router.include_router(self.__fillingsController.get_router())
    
    def get_router(self):
        return self.__router