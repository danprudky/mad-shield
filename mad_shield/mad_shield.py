from .configers import AgentLoader
from .agents.componentAgent import ComponentAgent
from .mad import *


def load_alert(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class MadShield:
    def __init__(self, agent_config_path: str, max_debate_rounds: int) -> None:
        self.components = [
            ComponentAgent(component)
            for component in AgentLoader(agent_config_path).load().items()
        ]
        self.mad = MultiAgentDebate(self.components, max_debate_rounds)
        self.mad.load_agents()
        self.mad.load_workforce()

    def go(self, alert_path: str) -> None:
        alert = load_alert(alert_path)
        self.mad.debate(alert)

        #from .command import Command
        # commands: List[Command] =
        # for command in commands:
        #    command.component.execute(command.command)
