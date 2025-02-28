from mad_shield.mad.agents.debate import DebateAgent

from typing import TYPE_CHECKING

from ..prompts.lawyer import *

if TYPE_CHECKING:
    from mad_shield.agents import ComponentAgent
    from mad_shield.mad import MultiAgentDebate


class LawyerAgent(DebateAgent):
    def __init__(self, component: "ComponentAgent", mad: "MultiAgentDebate") -> None:
        self.component = component

        super().__init__(mad, component.name + "_lawyer", "lawyer")

    def get_init_msg(self) -> str:
        return init_prompt(self.component.name, self.component.description)

    def react(self, proposal_summary: str) -> str:
        # Load message and create proposals or agree
        msg = react_prompt(proposal_summary)
        response = self.step(msg)
        return str(response.msgs[0].content)

    def propose_solution(self, alert: str) -> str:
        msg = propose_prompt(alert)
        response = self.step(msg)
        return str(response.msgs[0].content)
