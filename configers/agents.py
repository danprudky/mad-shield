from configers.loader import ConfigLoader


class AgentLoader(ConfigLoader):
    def __init__(self, config_path="config/agents.yaml") -> None:
        super().__init__(config_path)

    def load(self) -> dict:
        return self.config["agents"]
