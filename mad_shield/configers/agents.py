from typing import cast

from .loader import ConfigLoader


class AgentLoader(ConfigLoader):
    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)

    def load(self) -> dict[str, list[str]]:
        return cast(dict[str, list[str]], self.config["agents"])
