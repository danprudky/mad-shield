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
        
        "SUMMARIZATION FORMAT FOR FIRST ROUND PROPOSALS:\n"
        "```\n"
        "Here are the suggestions of the lawyer agents:\n"
        "<agent> agent suggests:\n"
        "  [\n"
        "    (<executable cli command>, <justification>),\n"
        "    ...\n"
        "  ]\n"
        "```\n\n"
        
        "SUMMARIZATION FORMAT FOR HIGHER ROUND PROPOSALS:\n"
        "```\n"
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
        "```\n"
    )

def summarize_prompt(proposals: str) -> str:
    """
    Generates a prompt for summarizing agent responses in a multi-agent debate.

    This function constructs a prompt that instructs a summarizer agent
    to analyze and summarize the current state of the debate based on the received proposals.
    The summarizer should determine the current debate round and extract key insights.

    Args:
        proposals (str): A string containing the agent proposals from the current round.

    Returns:
        str: A formatted prompt instructing how to summarize the proposals
             and extract relevant insights for the next debate round.

    The prompt includes:
    - Instructions to determine the current debate round.
    - A request to summarize agent proposals.
    - An implicit expectation to track the debate's progress.
    """
    return TextPrompt(
        "Calculate the round number and base on that summarize the following agent responses to the incoming attack: "
        f"{proposals}"
    )