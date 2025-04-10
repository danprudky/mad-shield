import textwrap

from camel.prompts import TextPrompt


def init_prompt(component_list: str) -> str:
    """
    Generates an initial prompt for a multi-agent debate summarization process.

    This function constructs a structured prompt that defines the role of a summarizer
    in a debate involving multiple agents representing different components.
    The summarizer is responsible for aggregating proposals, structuring opinions,
    and tracking the approval or discussion status of each suggestion.

    Args:
        component_list (str): A comma-separated string of component names that the agents represent.

    Returns:
        str: A formatted prompt string that outlines the summarization rules, structure, and expected output formats.

    The prompt includes:
    - The identity of the summarizer and its responsibilities.
    - Rules for determining whether proposals are approved or require further discussion.
    - A structured format for summarizing proposals in the first round.
    - A structured format for summarizing discussions and approvals in higher rounds.
    """
    return TextPrompt(
        "YOUR IDENTITY:\n"
        f"I need you to be a Summarizer in a multi-agent debate in which there are lawyer agents representing the {component_list} components and a coordinator. "
        "Your sole role is to aggregate the proposals and reactions after each debate round. You do not control or direct the debate.\n\n"
        
        "SUMMARIZATION RULES:\n"
        "1. If every agent agrees on a proposal, you mark it as APPROVED. If not, the proposal remains under discussion.\n\n"
    )

def summarize_prompt(proposals: str, is_first_round: bool) -> str:
    """
    Generates an optimized prompt for summarizing agent responses in a multi-agent debate.

    This function constructs a prompt that instructs a summarizer agent
    to analyze and summarize the current state of the debate efficiently.

    Args:
        proposals (str): A string containing the agent proposals from the current round.
        is_first_round (bool): Whether the current round is the first round.

    Returns:
        str: A formatted prompt instructing the summarizer to extract key insights concisely.
    """
    if is_first_round:
        response_format = textwrap.dedent(
            "Suggestions of the lawyer agents:\n"
            "<agent> agent suggests:\n"
            "  [\n"
            "    (<executable cli command>, <justification>),\n"
            "    ...\n"
            "  ]\n"
        )
    else:
        response_format = textwrap.dedent(
            "Here are the suggestions of the lawyer agents:\n"
            "<agent> agent suggests:\n"
            "  [\n"
            "    (<executable cli command>, <justification>) - APPROVED,\n"
            "    ...\n"
            "  ]\n"
            "Suggestions under discussion:\n"
            "<agent> suggests:\n"
            "  [ (<executable cli command>, <justification>), ... ],\n"
            "  but is opposed by <agent> because <reason>, and suggests alternative:\n"
            "  [ (<executable cli command>, <justification>), ... ]\n"
        )

    return TextPrompt(
        "Summarize the ALL following agent proposals efficiently into this format:\n"
        + response_format +
        "\n"
        "Focus on key actions and justifications, avoiding unnecessary details. If multiple agents suggest same command"
        "wrap it together.\n\n"
        f"Proposals:\n{proposals}"
    )