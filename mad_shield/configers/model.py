from camel.configs import GroqConfig, ChatGPTConfig
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs.base_config import BaseConfig
from typing import Optional

from .loader import ConfigLoader


class ModelLoader(ConfigLoader):
    def __init__(self, config_path: str = "mad_shield/config/models.yaml") -> None:
        super().__init__(config_path)
        self.model_configs = self.config["models"]

    # def __get_model_config(self) -> Optional[BaseConfig]:
    #    platform_name = self.model_config["platform_name"].lower()
    #    method_name = f"_get_{platform_name}_config"
    #    if hasattr(self, method_name):
    #        return getattr(self, method_name)()
    #    return None

    # def _get_groq_config(self) -> GroqConfig:
    #    return GroqConfig(
    #        temperature=self.model_config["temperature"],
    #        top_p=self.model_config["top_p"],
    #        n=self.model_config["n"],
    #        max_tokens=self.model_config["max_tokens"],
    #    )

    def gpt_4o_mini(self) -> BaseModelBackend:
        model_config = self.model_configs["gpt_4o_mini"]

        config = ChatGPTConfig(
            temperature=model_config["temperature"],
            top_p=model_config["top_p"],
            n=model_config["n"],
            max_tokens=model_config["max_tokens"],
        )

        return ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
            api_key=self.api_key,
            model_config_dict=config.as_dict(),
        )

    # def load(self) -> BaseModelBackend:
    #    platform_name = self.model_config["platform_name"]
    #    platform_type = getattr(ModelPlatformType, platform_name.upper())

    #    config = self.__get_model_config()
    #    if config is None:
    #        raise ValueError("Konfigurační metoda neexistuje!")

    #    return ModelFactory.create(
    #        model_platform=platform_type,
    #        model_type=self.model_config["model_type"],
    #        api_key=self.api_key,
    #        model_config_dict=config.model_dump(),
    #    )
