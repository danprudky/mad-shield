from enum import Enum

from .debate_agent import DebateAgent

from typing import TYPE_CHECKING, Tuple

from ..prompts.lawyer_prompts import *

if TYPE_CHECKING:
    from ...agents import ComponentAgent
    from .. import MultiAgentDebate


class LawyerAction(Enum):
    PROPOSE = "propose"
    CRITICIZE = "criticize"
    CORRECT = "correction"


class LawyerAgent(DebateAgent):
    def __init__(self, component: "ComponentAgent", mad: "MultiAgentDebate") -> None:
        self.component = component

        super().__init__(mad, component.name + "_lawyer")

    def get_init_msg(self) -> str:
        return init_prompt(self.component.name, self.component.description)

    def act(self, action: LawyerAction, additional_info: str) -> Tuple[str, str]:
        prompt = self._select_prompt(action, additional_info)
        return self.role, self.sent_prompt(prompt)

    def _select_prompt(self, action: LawyerAction, additional_info: str) -> str:
        if action == LawyerAction.PROPOSE:
            return propose_prompt(
                attack_alert=additional_info, component_name=self.component.name
            )
        elif action == LawyerAction.CRITICIZE:
            return react_prompt(
                proposals_summary=additional_info, component_name=self.component.name
            )
        elif action == LawyerAction.CORRECT:
            return react_correct_prompt(
                proposals_summary=additional_info, component_name=self.component.name
            )
        else:
            raise ValueError(f"Unknown action: {action}")
