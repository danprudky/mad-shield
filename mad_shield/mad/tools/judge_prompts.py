from camel.prompts import TextPrompt


def init_prompt(component_list: str) -> str:
    """
    Generates the initial prompt for coordinating a multi-agent debate.

    This function constructs a structured prompt that defines the role of a judge
    in a debate involving multiple agents, each representing different components.
    The judge coordinates the debate by gathering proposals, summarizing them,
    collecting opinions, and determining consensus among the agents.

    Args:
        component_list (str): A comma-separated string of component names representing the agents.

    Returns:
        str: A formatted prompt string outlining the debate rules, structure, and expected summarization formats.

    The prompt includes:
    - The judge's identity as the debate coordinator.
    - A step-by-step debate algorithm detailing how proposals and opinions are processed.
    - Rules for summarizing agent responses.
    - Specific formats for final approved proposals.
    """
    return TextPrompt(
        "ROLE:\n"
        f"You are the **Judge** in a multi-agent debate. Your task is to oversee a discussion between **lawyer agents**, each representing one of the following components: {component_list}.\n\n"

        "OBJECTIVE:\n"
        "Lawyer agents will debate the **best set of executable commands** to protect the system against an incoming attack. Your responsibilities are:\n"
        "1. **Determine whether consensus has been reached** at the end of each round.\n"
        "2. **End the debate** if consensus is reached or if the maximum number of rounds is exceeded.\n"
        "3. **Respond in the correct format** based on the debate's outcome.\n\n"

        "CONSENSUS RULES:\n"
        "- Consensus is reached if **all lawyer agents agree** on all proposals, and no proposals remain under discussion.\n"
        "- If consensus is reached, respond using the **FINAL PROPOSALS FORMAT**.\n"
        "- If consensus **is not reached** and the debate ends due to the maximum number of rounds, respond with the same format but **omit proposals still under discussion**.\n"
        "- If consensus **is not reached** and the debate is still ongoing, respond with: **'DEBATE HAS TO CONTINUE'**.\n\n"
        
        "FINAL PROPOSALS FORMAT:\n"
        
        "DEBATE IS OVER!\n"
        "Here are all approved suggestions of all agents:\n"
        "  [\n"
        "    (<agent>, <executable cli command>),\n"
        "    (<agent>, <executable cli command>),\n"
        "  ]\n"
        "...",
    )

