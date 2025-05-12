import textwrap

from camel.prompts import TextPrompt


def init_prompt(component_list: str) -> TextPrompt:
    return TextPrompt(
        "ROLE:\n"
        f"You are the **Judge** in a multi-agent debate between the following lawyer agents: {component_list}.\n\n"
        "OBJECTIVE:\n"
        "Lawyer agents are collaborating to determine the most effective **CLI commands** to defend the system.\n"
        "You coordinate the debate and track progress toward consensus.\n\n"
        "YOUR RESPONSIBILITIES:\n"
        "1. Determine whether full **consensus** has been reached.\n"
        "2. End the debate if consensus is reached or the maximum number of rounds is completed.\n"
        "3. Respond with the correct format based on debate status.\n\n"
        "CONSENSUS RULES:\n"
        "- Consensus is reached when **all lawyer agents approve all proposed commands**.\n"
        "- If multiple agents independently propose the same command, merge them as: 'More agents'.\n"
        "- Do NOT include commands still being discussed or without full approval.\n\n"
    )


def judge_debate_prompt(proposal_summary: str, is_last_round: bool) -> TextPrompt:

    if is_last_round:
        return TextPrompt(
            "Final round reached. Apply CONSENSUS RULES.\n"
            "Select only the proposals **approved by all agents**.\n"
            "Omit anything still under discussion.\n\n"
            "RESPONSE FORMAT:\n" + get_response_format() + "\nPROPOSALS:\n"
            f"{proposal_summary}"
        )
    else:
        return TextPrompt(
            "Review current round proposals.\n"
            "1. Check if **all agents approved all commands**.\n"
            "2. If yes, debate is over. Respond with RESPONSE FORMAT.\n"
            "3. If not, respond with: **DEBATE HAS TO CONTINUE**.\n\n"
            "RESPONSE FORMAT:\n" + get_response_format() + "\nPROPOSALS:\n"
            f"{proposal_summary}"
        )


def get_response_format() -> str:
    return textwrap.dedent(
        "   DEBATE IS OVER!\n"
        "   Here are all fully approved commands by all agents:\n"
        "   [\n"
        "       (<agent>, <cli command>),\n"
        "       (<agent>, <cli command>),\n"
        "       ...\n"
        "   ]\n"
    )
