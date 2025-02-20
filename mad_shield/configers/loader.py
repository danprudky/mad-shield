import os
import yaml
from dotenv import load_dotenv


class ConfigLoader:
    """Třída pro načtení konfigurace."""

    def __init__(self, config_path: str) -> None:
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
