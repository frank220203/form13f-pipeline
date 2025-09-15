from google import genai
from typing import List

from domain.config_manager import ConfigManager
from domain.usecases.services.prompt_service import PromptService

class GeminiPrompt(PromptService):

    def __init__(self, settings: ConfigManager):
        self.__settings = settings
        self.__model = "gemini-2.5-flash"
        self.__client = genai.Client(api_key=self.__settings.get_google_api_key())

    async def get_token_count(self, request: str) -> str:
        count = self.__client.models.count_tokens(model=self.__model, contents=request)
        return count

    async def get_response(self, request: str) -> str:
        response = self.__client.models.generate_content(model=self.__model, contents=request).text
        return response
    
    async def get_naics(self, sins: List[str], type: str) -> str:
        format = self.__settings.get_naics_format()
        request = self.__settings.get_naics_prompt()
        request = request.format(sins=sins, sin=type, format=format)
        response = self.__client.models.generate_content(model=self.__model, contents=request).text
        cl_response = response.replace("```json", "")
        cl_response = cl_response.replace("```", "")
        return cl_response