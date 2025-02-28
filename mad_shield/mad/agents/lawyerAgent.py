from mad_shield.mad.agents.debateAgent import DebateAgent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.agents import ComponentAgent
    from mad_shield.mad import MultiAgentDebate


class LawyerAgent(DebateAgent):

    def __init__(self, component: "ComponentAgent", mad: "MultiAgentDebate") -> None:
        self.component = component

        super().__init__(mad, component.name + "_lawyer", "lawyer")

    def get_init_msg(self) -> str:
        return self.prompts["init"].format(
            component_name=self.component.name,
            component_description=self.component.description,
        )

    def _get_attack_msg(self, attack_alert: str) -> str:
        return self.prompts["attack"].format(attack_alert=attack_alert)

    def _get_react_msg(self, proposals_summary: str) -> str:
        return self.prompts["react"].format(proposals_summary=proposals_summary)

    def propose_solution(self, alert: str) -> str:
        msg = self._get_attack_msg(alert)
        response = self.step(msg)
        return str(response.msgs[0].content)

    def react(self, proposal_summary) -> str:
        # Load message and create proposals or agree
        msg = self._get_react_msg(proposal_summary)
        response = self.step(msg)
        return str(response.msgs[0].content)
