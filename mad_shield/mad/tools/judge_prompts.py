from camel.prompts import TextPrompt


def init_prompt(component_list: str, max_rounds: int) -> str:
    """
    Generates the initial prompt for coordinating a multi-agent debate.

    This function constructs a structured prompt that defines the role of a judge
    in a debate involving multiple agents, each representing different components.
    The judge coordinates the debate by gathering proposals, summarizing them,
    collecting opinions, and determining consensus among the agents.

    Args:
        component_list (str): A comma-separated string of component names representing the agents.
        max_rounds (int): The maximum number of rounds that the debate will run for.

    Returns:
        str: A formatted prompt string outlining the debate rules, structure, and expected summarization formats.

    The prompt includes:
    - The judge's identity as the debate coordinator.
    - A step-by-step debate algorithm detailing how proposals and opinions are processed.
    - Rules for summarizing agent responses.
    - Specific formats for final approved proposals.
    """
    return TextPrompt(
        "YOUR IDENTITY:\n"
        f"I need you to be a Coordinator in a multi-agent debate in which there are lawyer agents representing the {component_list} components. "
        "The debate should start immediately with the lawyer agents proposing their secure suggestions for the incoming attack alert. "
        "You are responsible for collecting these proposals, coordinating the subsequent rounds, and eventually ending the debate. "
        "I will provide you with the FINAL PROPOSALS FORMAT (which you must use to end the workforce task). \n\n"

        "FINAL PROPOSALS FORMAT:\n"
        "Here are all approved suggestions of all agents:\n"
        "  [\n"
        "    (<agent>, <executable cli command>),\n"
        "    (<agent>, <executable cli command>),\n"
        "  ]\n"
        "...",
    )