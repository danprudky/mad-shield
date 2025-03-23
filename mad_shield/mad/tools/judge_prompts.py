import textwrap


def init_prompt(component_list: str, max_round: int) -> str:
    """
    Generates the initial prompt for coordinating a multi-agent debate.

    This function constructs a structured prompt that defines the role of a judge
    in a debate involving multiple agents, each representing different components.
    The judge coordinates the debate by gathering proposals, summarizing them,
    collecting opinions, and determining consensus among the agents.

    Args:
        component_list (str): A comma-separated string of component names representing the agents.
        max_round (int): The maximum number of debate rounds allowed before termination.

    Returns:
        str: A formatted prompt string outlining the debate rules, structure, and expected summarization formats.

    The prompt includes:
    - The judge's identity as the debate coordinator.
    - A step-by-step debate algorithm detailing how proposals and opinions are processed.
    - Rules for summarizing agent responses.
    - Specific formats for final approved proposals.
    """
    return textwrap.dedent(
        "YOUR IDENTITY:"
        f"I need you to be a Coordinator in a multi-agent debate in which there are agents representing the {component_list} components and summarizer agent. "
        "You will be the judge and will ask agents about their proposals, after second round check if debate is not over "
        "and if not, then provide the opinions of the other agents to all of them. "
        "If everyone agrees with everything you will end the debate with 'THE DEBATE IS OVER'."
        
        "DEBATE ALGORITHM:"
        "1. Each lawyer agent asynchronously propose secure suggestions to incoming attack alert."
        "2. Summarizer agent summarize the proposals into SUMMARIZATION FORMAT FOR FIRST ROUND PROPOSALS."
        "3. Each lawyer agent asynchronously react on other lawyer agents proposals."
        "4. Summarizer agent summarize the reactions of lawyers into SUMMARIZATION FORMAT FOR HIGHER ROUND PROPOSALS."
        "5. If they all APPROVED all proposals then end debate with 'THE DEBATE IS OVER' and return debate in FINAL PROPOSALS FORMAT. "
        f"   Otherwise, repeat step 4 and 5, until they will all agree or debate round will reaches {max_round}."
        
        "SUMMARIZATION RULES:"
        "1. Only if every agent said they agree on other agent proposal, summarizer agent can mark it as APPROVED. Otherwise, you will invoke discussion of this proposal."
        "2. There will always be at least 2 rounds of debate (making proposals and agree on other agents proposals)."
        
        "FINAL PROPOSALS FORMAT:"
        "DEBATE IS OVER!"
        "Here are all approved suggestions of all agents:"
        "  ["
        "    (<agent>, <executable cli command>),"
        "    (<agent>, <executable cli command>),"
        "  ]"
        "..."
    )