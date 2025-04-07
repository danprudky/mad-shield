import logging
import time
import ast

from typing import List
from typing import TYPE_CHECKING

from camel.tasks.task import Task

from .agents import *
from .agents.summarizer import SummarizerAgent
from ..command import Command

if TYPE_CHECKING:
    from mad_shield.agents.componentAgent import ComponentAgent

logger = logging.getLogger("debate")

class MultiAgentDebate:
    def __init__(self, components: List["ComponentAgent"], max_rounds: int = 5) -> None:
        self.max_rounds = max_rounds
        self.components = components

        self.lawyers: List[LawyerAgent] = []
        self.summarizer = None
        self.judge = None
        self.workforce = None

    def load_agents(self):
        for component in self.components:
            self.lawyers.append(component.hire_lawyer(self))

        self.summarizer = SummarizerAgent(self)
        self.judge = JudgeAgent(self)

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)

    async def debate(self, alert: str) -> List[Command]:
        start = time.time()

        debate_round = 1
        is_consensus = False

        print("Max rounds: " + str(self.max_rounds))

        proposals = await self.judge.get_proposals(alert)
        print(f"\nProposals ready in: {time.time() - start} seconds")
        logger.info(f"{debate_round} round proposals:\n" + str(proposals))

        summarized = await self.summarizer.summarize(proposals, debate_round)
        print(f"\nFirst round summary ready in: {time.time() - start} seconds")
        logger.info(f"{debate_round} round summary:\n" + summarized)

        debate_round += 1
        while not is_consensus and debate_round <= self.max_rounds:

            reacts = await self.judge.get_reacts(summarized)
            print(f"\nReacts ready in: {time.time() - start} seconds")
            logger.info(f"{debate_round} round proposals:\n" + str(reacts))

            summarized = await self.summarizer.summarize(reacts, debate_round)
            print(f"\n{debate_round}. round summary ready in: {time.time() - start} seconds")
            logger.info(f"{debate_round} round summary:\n" + summarized)


            if debate_round <= 1:
                debate_round += 1
                continue

            round_result = self.judge.judge_debate(summarized)
            print(f"\nJudge result ready in: {time.time() - start} seconds")
            logger.info(f"{debate_round} round judge result:\n" + round_result)

            is_consensus = True if "OVER" in round_result else False

            debate_round += 1

        print(f"\n;Debating tasks: {time.time() - start} seconds")
        exit(43)

    def parse_debate_result(self, debate_result: str) -> list[Command]:
        """
        Parses the debate result and returns a list of Command objects.

        Args:
            debate_result (str): The debate output containing approved suggestions.

        Returns:
            list[Command]: A list of parsed commands assigned to their respective agents.
        """
        commands_list = []
        start = debate_result.find("[")
        end = debate_result.rfind("]")

        if start == -1 or end == -1:
            raise ValueError("Invalid debate result format.")

        cleaned_result = debate_result[start:end + 1]
        for lawyer in self.lawyers:
            cleaned_result = cleaned_result.replace(lawyer.role, f"'{lawyer.role}'")

        try:
            approved_commands = ast.literal_eval(cleaned_result)
        except (SyntaxError, ValueError) as e:
            raise ValueError(f"Error parsing debate result: {e}")

        for agent_name, command in approved_commands:
            lawyer_candidates = [agent for agent in self.lawyers if agent.role == agent_name]
            if len(lawyer_candidates) >= 1:
                commands_list.append(Command(lawyer_candidates[0].component, command))
            else:
                raise ValueError(f"Unknown agent: {agent_name}")

        return commands_list