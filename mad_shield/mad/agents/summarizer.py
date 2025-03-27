from camel.toolkits import FunctionTool
from typing import TYPE_CHECKING

from .debate import DebateAgent

from mad_shield.mad.tools.summarizer_prompts import *

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate

class SummarizerAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        agent_tools = [
            FunctionTool(summarize_prompt),
        ]

        super().__init__(mad, "summarizer", tools=agent_tools)

    def get_init_msg(self) -> str:
        return init_prompt(self.mad.get_components_in_str())