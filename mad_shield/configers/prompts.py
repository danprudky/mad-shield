from typing import cast

from .loader import ConfigLoader


class PromptLoader(ConfigLoader):
    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)

    def load(self) -> dict[str, str]:
        return cast(dict[str, str], self.config["prompts"])
