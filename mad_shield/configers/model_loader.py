from camel.configs import ChatGPTConfig
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType

from .config_loader import ConfigLoader


class ModelLoader(ConfigLoader):
    def __init__(self, config_path: str = "mad_shield/config/models.yaml") -> None:
        super().__init__(config_path)
        self.model_configs = self.config["models"]

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