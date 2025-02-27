from .debateAgent import DebateAgent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate

class JudgeAgent(DebateAgent):
    def __init__(self, mad: "MultiAgentDebate") -> None:
        super().__init__(mad, "judge", "judge", "llama-70b")

    def get_init_msg(self) -> str:
        return self.prompts["init"].format(
            component_list=self.mad.get_components_in_str()
        )

    def get_summarize_msg(self, proposals: str) -> str:
        return self.prompts["summarize"].format(proposals=proposals)

    def init_debate(self, alert: str) -> str:
        # Send problem to the lawyers
        # TODO Implement
        # TODO Debug print("Initializing debate about:\n" + alert)
        proposals = {}
        for lawyer in self.mad.lawyers:
            proposals[lawyer.component.name] = lawyer.propose_solution(alert)

        return "\n\n".join(f"{name}:\n{text}" for name, text in proposals.items())

    def summarize_debate(self, proposals: str) -> tuple[str, bool]:
        # Summarize debate and decide if it is solved
        # TODO Implement
        msg = self.get_summarize_msg(proposals)
        summary = self.step(msg).msgs[0].content
        return summary, self.is_debate_over(summary)

    def get_opinion(self, proposal_summary: str, debate_round: int) -> str:
        # Sending summary to agents and ask their opinion
        proposals = {}
        for lawyer in self.mad.lawyers:
            proposals[lawyer.component.name] = lawyer.react(proposal_summary)
        return "\n\n".join(f"{name}:\n{text}" for name, text in proposals.items())

    def is_debate_over(self, summary: str) -> bool:
        if "debate is over" in summary.lower():
            print("Debate over!")
            return True
        return False
        # return "over" in summary
