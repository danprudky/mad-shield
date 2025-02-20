from .agents import *
from ..command import Command
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.agents.componentAgent import ComponentAgent


class MultiAgentDebate:

    def __init__(self, components: List["ComponentAgent"], max_rounds: int = 2) -> None:
        self.max_rounds = max_rounds
        self.components = components

        self.lawyers: List[LawyerAgent] = []

        for component in self.components:
            self.lawyers.append(component.hire_lawyer(self))

        self.judge = JudgeAgent(self)

    def debate(self, alert: str) -> List[Command]:
        # TODO Implement
        print("Debating...")
        proposals = self.judge.init_debate(alert)

        debate_round = 1
        proposal_summary, is_over = self.judge.summarize_debate(proposals)
        print(f"Debate round {debate_round} is done")
        while not is_over and debate_round < self.max_rounds:
            debate_round += 1
            proposals = self.judge.get_opinion(debate_round)
            proposal_summary, is_over = self.judge.summarize_debate(proposals)
            print(f"Debate round {debate_round} is done")

        if not is_over:
            print("Debate ends by max rounds reached")

        print(proposal_summary)

        # Summarizer extern commands
        # TODO Implement
        executable_commands = [
            ["ssh", "ls -h"],
            ["ssh", "ls"],
            ["firewall", "dir"],
        ]

        result = []
        for component, command in executable_commands:
            c = next((c for c in self.components if c.name == component), None)
            if c is None:
                raise ValueError(f"Component '{component}' not found")
            result.append(Command(c, command))
        return result

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)
