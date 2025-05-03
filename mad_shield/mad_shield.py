import asyncio
import json
import os
from typing import Set

from .app_config import app_config
from .configers import AgentLoader
from .agents.component_agent import ComponentAgent
from .mad import *


def load_alert(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class MadShield:
    def __init__(self, agent_config_path: str = "mad_shield/config/agents.yaml") -> None:
        self.agent_config_path = agent_config_path
        self._processed_alerts: Set[str] = set()
        self._last_offset = 0

        self._load_components()
        self._load_mad()

    def _load_components(self) -> None:
        self.components = [
            ComponentAgent(component)
            for component in AgentLoader(self.agent_config_path).load().items()
        ]

    def _load_mad(self) -> None:
        self.mad = MultiAgentDebate(self.components)

    async def defend(self, alert: str) -> None:
        commands = await self.mad.debate(alert)

        for command in commands:
            command.component.execute(command.command)

    async def run_service(self, alerts_file: str) -> None:
        if app_config().debug:
            print("MadShield running in passive mode. Waiting for alerts...")

        while True:
            if not os.path.exists(alerts_file):
                await asyncio.sleep(app_config().polling_interval)
                continue

            alert = self._read_new_alerts(alerts_file)

            if alert is None:
                await asyncio.sleep(app_config().polling_interval)
                continue

            await self.defend(alert)

            if app_config().debug:
                print("Alert processed.")

            if app_config().process_one:
                break

            self._reset()
            await asyncio.sleep(app_config().polling_interval)

    def _read_new_alerts(self, alerts_file: str) -> str | None:
        with open(alerts_file, 'r') as f:
            f.seek(self._last_offset)

            while True:
                line = f.readline()
                self._last_offset = f.tell()
                if not line:
                    break #EOF

                if not line.strip():
                    continue

                try:
                    alert = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                alert_id = self._get_alert_id(alert)
                if alert_id not in self._processed_alerts:
                    self._processed_alerts.add(alert_id)
                    if app_config().debug:
                        print(f"Alert {alert_id} loaded")
                    return json.dumps(alert)
                elif app_config().debug:
                    print(f"Alert {alert_id} already processed.")
        return None


    async def _process_alert_batch(self, batch: list[str]) -> None:
        for alert_str in batch:
            if app_config().debug:
                print("Alert found:", alert_str)

            await self.defend(alert_str)

            if app_config().debug:
                print("Alert processed.")

            if app_config().process_one:
                break

    @staticmethod
    def _get_alert_id(alert: dict) -> str:
        return f"{alert.get('src_ip')}_{alert.get('proto')}_{alert.get('alert', {}).get('signature_id')}_{alert.get('direction')}"


    def _reset(self) -> None:
        self._load_components()
        self._load_mad()
