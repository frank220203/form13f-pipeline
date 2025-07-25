from abc import ABC, abstractmethod

class ConfigManager(ABC):
    @abstractmethod
    def get_api_version(self) -> str:
        pass

    @abstractmethod
    def get_environment(self) -> str:
        pass

    @abstractmethod
    def get_project_name(self) -> str:
        pass

    @abstractmethod
    def get_user_agent(self) -> str:
        pass

    @abstractmethod
    def get_kafka_broker_ip(self) -> str:
        pass

    @abstractmethod
    def get_kafka_topic(self) -> str:
        pass

    @abstractmethod
    def get_kafka_group_pf(self) -> str:
        pass