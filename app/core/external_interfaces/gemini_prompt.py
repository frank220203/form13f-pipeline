import google.generativeai as genai
from typing import List
from google.generativeai.generative_models import GenerativeModel
from api.deps import di_manager
from domain.config_manager import ConfigManager
from domain.usecases.services.prompt_service import PromptService

class GeminiPrompt(PromptService):

    __model: GenerativeModel

    def __init__(self, settings: ConfigManager):
        self.__settings = di_manager.get_config_manager()
        genai.configure(api_key=self.__settings.get_google_api_key())
        self.__model = genai.GenerativeModel("gemini-2.5-flash")

    async def get_response(self, request: str) -> str:
        response = self.__model.generate_content(request).text
        return response
    
    async def get_naics(self, sins: List[str]) -> str:
        request = f"{sins}에 대응되는 naics 값을 숫자로만 알려주는데 List 형식으로 알려줘"
        return self.__model.generate_content(request).text