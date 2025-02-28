import os
from camel.tasks import Task

from .agents import *
from ..command import Command
from typing import List
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from mad_shield.agents.componentAgent import ComponentAgent

class MultiAgentDebate:

    def __init__(self, components: List["ComponentAgent"], max_rounds: int = 5) -> None:
        self.max_rounds = max_rounds
        self.components = components

        self.lawyers: List[LawyerAgent] = []

        for component in self.components:
            self.lawyers.append(component.hire_lawyer(self))

        self.judge = JudgeAgent(self)


    def debate(self, alert: str) -> List[Command]:
        # TODO Implement
        print("Debating...")
        debate_round = 1

        proposals = self.judge.init_debate(alert)
        proposal_summary, is_over = self.judge.summarize_debate(proposals)
        logging.debug(f"\n\n\nProposals in {debate_round}:\n{proposals}")
        logging.debug(f"Proposal summary:\n{proposal_summary}")

        print(f"Debate round {debate_round} is done")
        while not is_over and debate_round < self.max_rounds:
            debate_round += 1
            proposals = self.judge.get_opinion(proposal_summary, debate_round)
            logging.debug(f"\n\n\nProposals in {debate_round}:\n{proposals}")
            logging.debug(f"Proposal summary:\n{proposal_summary}")

            proposal_summary, is_over = self.judge.summarize_debate(proposals)
            logging.debug(f"Debate round {debate_round} is done")

        if not is_over:
            logging.debug("Debate ends by max rounds reached")

        logging.debug(proposal_summary)

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

    def task(self):
        task = Task()