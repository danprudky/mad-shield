from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate


def judge_coordination_process(mad: "MultiAgentDebate", alert: str) -> str:
    r"""Function to define the judge coordination process. Base on this function, judge will coordinate the debate.

    Args:
        mad (MultiAgentDebate): Multi-agent debate, where judge is coordinator
        alert (str): Warning alert

    Returns:
        integer: The summary of the debate process, list of commands, agreed by all lawyer agents
    """

    proposals = mad.judge.init_debate(alert)
    proposal_summary, is_over = mad.judge.summarize_debate(proposals)

    debate_round = 1
    while not is_over and debate_round < mad.max_rounds:
        debate_round += 1
        proposals = mad.judge.get_opinion(proposal_summary, debate_round)

        proposal_summary, is_over = mad.judge.summarize_debate(proposals)

    return proposal_summary
