import time
import re

from typing import List, Tuple
from typing import TYPE_CHECKING

from .agents import *
from ..app_config import app_config
from ..command import Command

if TYPE_CHECKING:
    from ..agents.component_agent import ComponentAgent


class MultiAgentDebate:
    def __init__(self, components: List["ComponentAgent"]) -> None:
        self.components = components
        self.lawyers = [component.hire_lawyer(self) for component in self.components]
        self.judge = JudgeAgent(self)

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)

    async def debate(self, alert: str) -> List[Command]:

        if app_config().debug:
            start_time = time.time()
            self._log(f"Max rounds: {app_config().max_debate_rounds}", 0.0, "")
        else:
            start_time = None

        proposals = await self._get_initial_proposals(alert, start_time)
        round_result = ""

        for round_number in range(2, app_config().max_debate_rounds + 1):
            proposals = await self._get_reacts_to_proposals(
                proposals, round_number, start_time
            )

            round_result = self.judge.judge_debate(
                proposals, is_last_round=(round_number == app_config().max_debate_rounds)
            )

            if app_config().debug:
                self._log_result(round_number, start_time, round_result)

            if "OVER" in round_result:
                return self._parse_final_result(round_result)

        # If we exit loop without consensus
        return self._parse_final_result(round_result)

    async def _get_initial_proposals(self, alert: str, start_time: float|None) -> str:
        proposals = await self.judge.get_proposals(alert)
        result = self._format_proposals(proposals)

        if app_config().debug:
            self._log("Proposals ready", start_time, result)
        return result

    async def _get_reacts_to_proposals(
        self, proposals: str, round_number: int, start_time: float|None
    ) -> str:
        if round_number == 2:
            new_proposals = await self.judge.get_reacts(proposals)
        else:
            new_proposals = await self.judge.get_reacts_and_corrections(proposals)
        result = self._format_proposals(new_proposals)

        if app_config().debug:
            self._log("Reacts ready", start_time, result)

        return result

    def _parse_final_result(self, debate_result: str) -> List[Command]:
        commands_list = []

        start = debate_result.find("[")
        end = debate_result.rfind("]")

        if start == -1 or end == -1:
            raise ValueError("Invalid debate result format.")

        cleaned_result = debate_result[start:end + 1]

        pattern = re.compile(r"\(\s*([a-zA-Z0-9_]+)\s*,\s*(.*?)\s*\)")
        matches = pattern.findall(cleaned_result)

        if not matches:
            raise ValueError("No valid (role, command) pairs found.")

        for role, command in matches:

            if role.lower() == "more agents":
                component = self.lawyers[0].component
            else:
                matched_lawyers = [
                    agent for agent in self.lawyers
                    if agent.component.name in role
                ]

                if not matched_lawyers:
                    raise ValueError(f"Unknown agent role: {role}")
                component = matched_lawyers[0].component

            commands_list.append(Command(component, command))

        return self._normalize_commands(commands_list)

    @staticmethod
    def _normalize_commands(commands: List[Command]) -> List[Command]:
        seen = set()
        unique_commands = []

        for cmd in commands:
            normalized = cmd.command.strip()
            if normalized.startswith("sudo "):
                normalized = normalized[5:].strip()

            if normalized not in seen:
                seen.add(normalized)
                unique_commands.append(Command(cmd.component, normalized))

        return unique_commands

    @staticmethod
    def _format_proposals(proposals: List[Tuple[str, str]]) -> str:
        return "\n\n".join(proposal for _, proposal in proposals)

    @staticmethod
    def _log(message: str, start_time: float | None, content: str) -> None:
        print(f"\n{message}")
        if start_time:
            print(f"Time elapsed: {time.time() - start_time:.2f}s")
        if content:
            print(content)

    def _log_result(
        self, round_number: int, start_time: float | None, result: str
    ) -> None:
        self._log(f"{round_number}. round judge result", start_time, result)
