from camel.configs import GroqConfig
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType
from camel.configs.base_config import BaseConfig
from typing import Optional

from configers.loader import ConfigLoader


class ModelLoader(ConfigLoader):
    def __init__(self, config_path="config/model.yaml") -> None:
        super().__init__(config_path)
        self.model_config = self.config["model"]

    def __get_model_config(self) -> Optional[BaseConfig]:
        platform_name = self.model_config["platform_name"].lower()
        method_name = f"_get_{platform_name}_config"
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        return None

    def _get_groq_config(self) -> GroqConfig:
        return GroqConfig(
            temperature=self.model_config["temperature"],
            top_p=self.model_config["top_p"],
            n=self.model_config["n"],
            max_tokens=self.model_config["max_tokens"],
        )

    def load(self) -> BaseModelBackend:
        platform_name = self.model_config["platform_name"]
        platform_type = getattr(ModelPlatformType, platform_name.upper())

        config = self.__get_model_config()
        if config is None:
            raise ValueError("Konfigurační metoda neexistuje!")

        return ModelFactory.create(
            model_platform=platform_type,
            model_type=self.model_config["model_type"],
            api_key=self.api_key,
            model_config_dict=config.model_dump(),
        )
