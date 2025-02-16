from .loader import ConfigLoader


class PromptLoader(ConfigLoader):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)

    def load(self) -> dict[str, str]:
        return self.config["prompts"]
