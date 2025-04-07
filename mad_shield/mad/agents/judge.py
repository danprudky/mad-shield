import asyncio
from typing import TYPE_CHECKING

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

    def judge_debate(self, proposal_summary: str):
        prompt = "Based on round summary evaluate whether all agents have approved all proposals. "
        "This is last debate round, pick all approved proposals and end the debate with FINAL PROPOSALS FORMAT "
        "as it is in your init message: "
        f"{proposal_summary}"

        response = self.step(prompt)
        return response.msgs[0].content