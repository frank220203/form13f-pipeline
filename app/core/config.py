from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from domain.config_manager import ConfigManager

class Settings(BaseSettings, ConfigManager):
    model_config = SettingsConfigDict(
        env_file="./core/env/.env",
        env_ignore_empty=True,
        extra="ignore"
    )
    API_VERSION: str
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    USER_AGENT: str
    KAFKA_BROKER_IP: str

    def get_api_version(self) -> str:
        return self.API_VERSION
    
    def get_environment(self) -> str:
        return self.ENVIRONMENT
    
    def get_project_name(self) -> str:
        return self.PROJECT_NAME
    
    def get_user_agent(self) -> str:
        return self.USER_AGENT
    
    def get_kafka_broker_ip(self) -> str:
        return self.KAFKA_BROKER_IP