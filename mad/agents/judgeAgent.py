from .debateAgent import DebateAgent


class JudgeAgent(DebateAgent):
    def __init__(self, mad) -> None:
        super().__init__(mad)
        for lawyer in mad.lawyers:
            lawyer.hi()

    def init_debate(self, alert: str) -> None:
        # Send problem to the lawyers
        # TODO Implement
        print("Initializing debate about " + alert)
        for lawyer in self.mad.lawyers:
            lawyer.propose_solution(alert)

    def summarize_debate(self, debate_round: int) -> tuple[str, bool]:
        # Summarize debate and decide if it is solved
        # TODO Implement
        print("Summarizing debate...")
        summary = "Debate summary"
        return summary, self.is_debate_over(summary)

    def get_opinion(self, debate_round: int):
        # Sending summary to agents and ask their opinion
        # TODO Implement
        print("Getting agents opinion...")
        for lawyer in self.mad.lawyers:
            lawyer.react(debate_round)

    def is_debate_over(self, summary: str):
        if "over" in summary.lower():
            print("Debate over!")
            return True

        # return "over" in summary
