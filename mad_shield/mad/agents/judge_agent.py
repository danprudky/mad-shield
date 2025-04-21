import asyncio
from typing import TYPE_CHECKING, List, Tuple

from .debate_agent import DebateAgent

from ..prompts.judge_prompts import *
from .lawyer_agent import LawyerAction

if TYPE_CHECKING:
    from ..mad import MultiAgentDebate


class JudgeAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        super().__init__(mad, "judge")

    def get_init_msg(self) -> str:
        return init_prompt(self.mad.get_components_in_str())

    async def get_lawyer_responses(
        self, action: LawyerAction, additional_info: str
    ) -> List[Tuple[str, str]]:
        """
        General method to gather responses for different actions (propose, criticize, correct).

        Args:
            action (LawyerAction): The action type (propose, criticize, correct).
            additional_info (str): The text (alert or proposal summary) to process.

        Returns:
            List[Tuple[str, str]]: List of responses from each agent.
        """
        responses = await asyncio.gather(
            *[
                asyncio.to_thread(agent.act, action, additional_info)
                for agent in self.mad.lawyers
            ]
        )
        return responses

    async def get_proposals(self, alert: str) -> List[Tuple[str, str]]:
        return await self.get_lawyer_responses(LawyerAction.PROPOSE, alert)

    async def get_reacts(self, proposal_summary: str) -> List[Tuple[str, str]]:
        return await self.get_lawyer_responses(LawyerAction.CRITICIZE, proposal_summary)

    async def get_reacts_and_corrections(
        self, proposal_summary: str
    ) -> List[Tuple[str, str]]:
        return await self.get_lawyer_responses(LawyerAction.CORRECT, proposal_summary)

    def judge_debate(self, proposal_summary: str, is_last_round: bool) -> str:
        prompt = judge_debate_prompt(proposal_summary, is_last_round)
        return self.sent_prompt(prompt)
