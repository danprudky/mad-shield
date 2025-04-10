import asyncio
from typing import TYPE_CHECKING, List

from .debate import DebateAgent

from mad_shield.mad.tools.judge_prompts import *

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate


class JudgeAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        super().__init__(mad, "judge")

    def get_init_msg(self) -> str:
        return init_prompt(self.mad.get_components_in_str())

    async def get_proposals(self, alert: str):
        responses = await asyncio.gather(
            *[asyncio.to_thread(agent.propose, alert) for agent in self.mad.lawyers]
        )
        return responses

    async def get_reacts(self, proposal_summary: str):
        responses = await asyncio.gather(
            *[asyncio.to_thread(agent.criticize, proposal_summary) for agent in self.mad.lawyers]
        )
        return responses

    async def get_reacts_and_corrections(self, proposal_summary: str):
        responses = await asyncio.gather(
            *[asyncio.to_thread(agent.criticize_with_self_correction, proposal_summary) for agent in self.mad.lawyers]
        )
        return responses

    def judge_debate(self, proposal_summary: str, last_round: bool):
        prompt = judge_debate_prompt(proposal_summary, last_round)
        response = self.step(prompt)
        return response.msgs[0].content