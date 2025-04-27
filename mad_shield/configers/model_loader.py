import os
from dotenv import load_dotenv

from camel.configs import ChatGPTConfig
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType

from .config_loader import ConfigLoader

model_types = {
    "gpt-4o-mini" : ModelType.GPT_4O_MINI,
    "o3-mini" : ModelType.O3_MINI,
}

class ModelLoader(ConfigLoader):
    def __init__(self, config_path: str = "mad_shield/config/models.yaml") -> None:
        super().__init__(config_path)
        self.model_configs = self.config["models"]

        load_dotenv()
        self.default_model = os.getenv("DEFAULT_MODEL_TYPE", "gpt-4o-mini")
        self.default_temperature = os.getenv("DEFAULT_TEMPERATURE")

    def load_model(self) -> BaseModelBackend:
        model_config = self.model_configs[self.default_model]
        temperature = model_config["temperature"] if self.default_temperature is None else self.default_temperature

        config = ChatGPTConfig(
            temperature=temperature,
            top_p=model_config["top_p"],
            n=model_config["n"],
            max_tokens=model_config["max_tokens"],
        )

        return ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=model_types[self.default_model],
            api_key=self.api_key,
            model_config_dict=config.as_dict(),
        )