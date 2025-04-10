from camel.toolkits import FunctionTool
from typing import TYPE_CHECKING, List, Tuple

from .debate import DebateAgent

from mad_shield.mad.tools.summarizer_prompts import *

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate

class SummarizerAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        super().__init__(mad, "summarizer")

    def get_init_msg(self) -> str:
        return init_prompt(self.mad.get_components_in_str())

    async def summarize(self, proposals: List[Tuple[str, str]], debate_round: int) -> str:
        prompt = summarize_prompt(str(proposals), debate_round == 1)
        response = self.step(prompt)
        return response.msgs[0].content