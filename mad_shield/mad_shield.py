import asyncio
import os

from .configers import AgentLoader
from .agents.componentAgent import ComponentAgent
from .configers.app import app_config
from .mad import *


def load_alert(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class MadShield:
    def __init__(self, agent_config_path: str) -> None:
        self.agent_config_path = agent_config_path

        self._load_components()
        self._load_mad()

    def _load_components(self) -> None:
        self.components = [
            ComponentAgent(component)
            for component in AgentLoader(self.agent_config_path).load().items()
        ]

    def _load_mad(self):
        self.mad = MultiAgentDebate(self.components)

    async def defend(self, alert_path: str) -> None:
        alert = load_alert(alert_path)
        commands = await self.mad.debate(alert)

        for command in commands:
            command.component.execute(command.command)

    async def run_service(self, alerts_dir: str = "alert", alert_extension: str = ".alert") -> None:
        if app_config().debug:
            print("MadShield running in passive mode. Waiting for alerts...")

        while True:
            alert_files = [
                f for f in os.listdir(alerts_dir) if f.endswith(alert_extension)
            ]

            if app_config().debug:
                print(alert_files)

            if alert_files:
                for filename in alert_files:
                    alert_path = os.path.join(alerts_dir, filename)

                    if app_config().debug:
                        print(f"Alert found: {alert_path}. Start defending...")

                    await self.defend(alert_path)

                    if app_config().debug:
                        print(f"Alert {filename} processed.")

                    if app_config().process_one:
                        return

                    os.remove(alert_path)
                    if app_config().debug:
                        print(f"Alert {filename} deleted.")

                    self._reset()
            await asyncio.sleep(app_config().polling_interval)

    def _reset(self):
        self._load_components()
        self._load_mad()
