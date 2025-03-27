from camel.toolkits import FunctionTool

from mad_shield.mad.agents.debate import DebateAgent

from typing import TYPE_CHECKING

from mad_shield.mad.tools.lawyer_prompts import *

if TYPE_CHECKING:
    from mad_shield.agents import ComponentAgent
    from mad_shield.mad import MultiAgentDebate


class LawyerAgent(DebateAgent):
    def __init__(self, component: "ComponentAgent", mad: "MultiAgentDebate") -> None:
        self.component = component

        agent_tools = [
            FunctionTool(propose_prompt),
            FunctionTool(react_prompt),
        ]

        super().__init__(mad, component.name + "_lawyer", tools=agent_tools)

    def get_init_msg(self) -> str:
        return init_prompt(self.component.name, self.component.description)