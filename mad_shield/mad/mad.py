import time
import ast
import re

from typing import List, Tuple
from typing import TYPE_CHECKING

from .agents import *
from ..command import Command

if TYPE_CHECKING:
    from mad_shield.agents.componentAgent import ComponentAgent


class MultiAgentDebate:
    def __init__(self, components: List["ComponentAgent"], max_rounds: int = 5) -> None:
        self.max_rounds = max_rounds
        self.components = components
        self.lawyers = [component.hire_lawyer(self) for component in self.components]
        self.judge = JudgeAgent(self)

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)

    async def debate(self, alert: str) -> List[Command]:

        start_time = time.time()  # TODO: DEBUG
        self._log(f"Max rounds: {self.max_rounds}", 0.0, "")  # TODO: DEBUG

        proposals = await self._get_initial_proposals(alert, start_time)
        round_result = ""

        for round_number in range(2, self.max_rounds + 1):
            proposals = await self._get_reacts_to_proposals(
                proposals, round_number, start_time
            )

            round_result = self.judge.judge_debate(
                proposals, is_last_round=(round_number == self.max_rounds)
            )
            self._log_result(round_number, start_time, round_result)

            if "OVER" in round_result:
                return self._parse_final_result(round_result)

        # If we exit loop without consensus
        return self._parse_final_result(round_result)

    async def _get_initial_proposals(self, alert: str, start_time: float) -> str:
        proposals = await self.judge.get_proposals(alert)
        result = self._format_proposals(proposals)
        self._log("Proposals ready", start_time, result)  # TODO: DEBUG
        return result

    async def _get_reacts_to_proposals(
        self, proposals: str, round_number: int, start_time: float
    ) -> str:
        if round_number == 2:
            new_proposals = await self.judge.get_reacts(proposals)
        else:
            new_proposals = await self.judge.get_reacts_and_corrections(proposals)
        result = self._format_proposals(new_proposals)
        self._log("Reacts ready", start_time, result)  # TODO: DEBUG
        return result

    def _parse_final_result(self, debate_result: str) -> List[Command]:
        commands_list = []

        start = debate_result.find("[")
        end = debate_result.rfind("]")

        if start == -1 or end == -1:
            raise ValueError("Invalid debate result format.")

        cleaned_result = debate_result[start:end + 1]

        # Find all (role, command) with regex
        pattern = re.compile(r"\(\s*([a-zA-Z0-9_]+)\s*,\s*(.*?)\s*\)")
        matches = pattern.findall(cleaned_result)

        if not matches:
            raise ValueError("No valid (role, command) pairs found.")

        for role, command in matches:
            matched_lawyers = [
                agent for agent in self.lawyers
                if agent.component.name in role
            ]

            if not matched_lawyers:
                raise ValueError(f"Unknown agent role: {role}")
            commands_list.append(Command(matched_lawyers[0].component, command))

        return commands_list

    @staticmethod
    def _format_proposals(proposals: List[Tuple[str, str]]) -> str:
        return "\n\n".join(proposal for _, proposal in proposals)

    @staticmethod
    def _log(message: str, start_time: float, content: str) -> None:  # TODO: DEBUG
        print(f"\n{message}")
        if start_time:
            print(f"Time elapsed: {time.time() - start_time:.2f}s")
        if content:
            print(content)

    def _log_result(
        self, round_number: int, start_time: float, result: str
    ) -> None:  # TODO: DEBUG
        self._log(f"{round_number}. round judge result", start_time, result)
