from typing import TYPE_CHECKING

from .debate import DebateAgent

from mad_shield.mad.tools.judge_prompts import *

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate


class JudgeAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        super().__init__(mad, "judge")

    def get_init_msg(self) -> str:
        return init_prompt(self.mad.get_components_in_str(), self.mad.max_rounds)