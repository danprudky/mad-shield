import os
import yaml
from dotenv import load_dotenv
from camel.configs import GroqConfig
from camel.models import ModelFactory, BaseModelBackend
from camel.types import ModelPlatformType


class ConfigLoader:
    """Třída pro načtení konfigurace modelu."""

    def __init__(self, config_path="config.yaml"):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.model_config = self.config["model"]

    def get_model_config(self):
        platform_name = self.model_config["platform_name"].lower()
        method_name = f"get_{platform_name}_config"
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        else:
            raise ValueError(f"Konfigurační metoda {method_name} neexistuje!")

    def get_groq_config(self) -> GroqConfig:
        return GroqConfig(
            temperature=self.model_config["temperature"],
            top_p=self.model_config["top_p"],
            n=self.model_config["n"],
            max_tokens=self.model_config["max_tokens"]
        )

    def get_model(self) -> BaseModelBackend:
        platform_name = self.model_config["platform_name"]
        platform_type = getattr(ModelPlatformType, platform_name.upper())

        return ModelFactory.create(
            model_platform=platform_type,
            model_type=self.model_config["model_type"],
            api_key=self.api_key,
            model_config_dict=self.get_model_config().dict(),
        )