import asyncio
import os

from .configers import AgentLoader
from .agents.componentAgent import ComponentAgent
from .mad import *


def load_alert(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class MadShield:
    def __init__(self, agent_config_path: str, max_debate_rounds: int) -> None:
        self.agent_config_path = agent_config_path
        self.max_debate_rounds = max_debate_rounds

        self._load_components()
        self._load_mad()

    def _load_components(self) -> None:
        self.components = [
            ComponentAgent(component)
            for component in AgentLoader(self.agent_config_path).load().items()
        ]

    def _load_mad(self):
        self.mad = MultiAgentDebate(self.components, self.max_debate_rounds)

    async def defend(self, alert_path: str) -> None:
        alert = load_alert(alert_path)
        commands = await self.mad.debate(alert)

        for command in commands:
            command.component.execute(command.command)

    async def run_service(self, alerts_dir: str = "alert", alert_extension: str = ".alert", poll_interval: int = 2) -> None:
        print("MadShield running in passive mode. Waiting for alerts...")
        while True:
            print(os.listdir(alerts_dir))
            alert_files = [
                f for f in os.listdir(alerts_dir) if f.endswith(alert_extension)
            ]
            if alert_files:
                for filename in alert_files:
                    alert_path = os.path.join(alerts_dir, filename)
                    print(f"Alert found: {alert_path}. Start defending...")
                    await self.defend(alert_path)
                    os.remove(alert_path)
                    print(f"Alert {filename} processed and deleted.")
                    self._reset()
            await asyncio.sleep(poll_interval)

    def _reset(self):
        self._load_components()
        self._load_mad()
