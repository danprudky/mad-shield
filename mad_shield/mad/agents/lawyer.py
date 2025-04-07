from camel.toolkits import FunctionTool

from mad_shield.mad.agents.debate import DebateAgent

from typing import TYPE_CHECKING, Tuple

from mad_shield.mad.tools.lawyer_prompts import *

if TYPE_CHECKING:
    from mad_shield.agents import ComponentAgent
    from mad_shield.mad import MultiAgentDebate


class LawyerAgent(DebateAgent):
    def __init__(self, component: "ComponentAgent", mad: "MultiAgentDebate") -> None:
        self.component = component

        super().__init__(mad, component.name + "_lawyer")

    def get_init_msg(self) -> str:
        return init_prompt(self.component.name, self.component.description)

    def propose(self, alert: str) -> Tuple[str, str]:
        prompt = propose_prompt(alert)
        response = self.step(prompt)
        return self.role, response.msgs[0].content

    def criticize(self, proposal_summary: str) -> Tuple[str, str]:
        prompt = react_prompt(proposal_summary)
        response = self.step(prompt)
        return self.role, response.msgs[0].content