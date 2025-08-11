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
    SEC_URL: str
    DATA_URL: str
    META_URL: str
    ISSUERS_URL: str
    TICKERS_URL: str
    SUBMISSIONS_URL: str
    KAFKA_BROKER_IP: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_PF: str
    MOBGO_DB_URL: str
    DOCUMENT_MODELS: str

    def get_api_version(self) -> str:
        return self.API_VERSION
    
    def get_environment(self) -> str:
        return self.ENVIRONMENT
    
    def get_project_name(self) -> str:
        return self.PROJECT_NAME
    
    def get_user_agent(self) -> str:
        return self.USER_AGENT
    
    def get_sec_url(self) -> str:
        return self.SEC_URL

    def get_data_url(self) -> str:
        return self.DATA_URL
    
    def get_meta_url(self) -> str:
        return self.META_URL
    
    def get_issuers_url(self) -> str:
        return self.ISSUERS_URL
    
    def get_data_url(self) -> str:
        return self.DATA_URL
    
    def get_meta_url(self) -> str:
        return self.META_URL
    
    def get_issuers_url(self) -> str:
        return self.ISSUERS_URL
    
    def get_tickers_url(self) -> str:
        return self.TICKERS_URL
    
    def get_submissions_url(self) -> str:
        return self.SUBMISSIONS_URL
    
    def get_kafka_broker_ip(self) -> str:
        return self.KAFKA_BROKER_IP
    
    def get_kafka_topic(self) -> str:
        return self.KAFKA_TOPIC
    
    def get_kafka_group_pf(self) -> str:
        return self.KAFKA_GROUP_PF
    
    def get_mongo_db_url(self) -> str:
        return self.MOBGO_DB_URL
    
    def get_document_models(self) -> str:
        return self.DOCUMENT_MODELS