import textwrap


def init_prompt(component_list: str, max_round: int) -> str:
    """
    Generates an initial prompt for a multi-agent debate coordination process.

    This function constructs a structured prompt that defines the role of a judge
    in a debate involving multiple agents representing different components.
    The judge coordinates the debate by gathering proposals, summarizing them,
    collecting opinions, and determining consensus among the agents.

    Args:
        component_list (str): A comma-separated string of component names that the agents represent.
        max_round (int): The maximum number of debate rounds allowed before termination.

    Returns:
        str: A formatted prompt string that outlines the debate rules, structure, and expected summarization formats.

    The prompt includes:
    - Identity of the judge as the debate coordinator.
    - A step-by-step debate algorithm, detailing how proposals and opinions should be processed.
    - Rules for summarizing agent responses.
    - Specific formats for first-round proposals, higher-round discussions, and final approved proposals.
    """
    return textwrap.dedent(
        "YOUR IDENTITY:"
        f"I need you to be a Coordinator in a multi-agent debate in which there are agents representing the {component_list} components. "
        "You will be the judge and will always summarize the proposals after each round of debate and then provide the opinions of the other agents. "
        "If everyone agrees with everything you will end the debate with 'THE DEBATE IS OVER'."
        
        "DEBATE ALGORITHM:"
        "1. Ask each lawyer agent for proposals to incoming attack alert."
        "2. Summarize the proposals into SUMMARIZATION FORMAT FOR FIRST ROUND PROPOSALS."
        "3. Send each lawyer this summary."
        "4. Summarize the opinions into SUMMARIZATION FORMAT FOR HIGHER ROUND PROPOSALS."
        "5. If they all APPROVED all proposals then end debate with 'THE DEBATE IS OVER'. "
        f"   Otherwise, repeat step 4 and 5, until they will all agree or debate round will reaches {max_round}."
        "7. In the end return last generated summary in same format."
        
        "SUMMARIZATION RULES:"
        "1. If every agent said they agree on other agent proposal, you can mark it as APPROVED. Otherwise, you will add this proposal into discussion."
        "2. There will always be at least 2 rounds of debate (making proposals and agree on other agents proposals)."
        
        "SUMMARIZATION FORMAT FOR FIRST ROUND PROPOSALS:"
        "```"
        "Here are the suggestions of the other agents:"
        "<agent> agent suggests:"
        "  ["
        "    (<executable cli command>, <justification>),"
        "    (<executable cli command>, <justification>),"
        "  ]"
        "..."
        "If you disagree with something or have a suggestion for improvement, you can edit the action suggestion"
        "```"
        
        "SUMMARIZATION FORMAT FOR HIGHER ROUND PROPOSALS:"
        "```"
        "Here are the suggestions of the other agents:"
        "<agent> agent suggests:"
        "  ["
        "    (<executable cli command>, <justification>) - APPROVED,"
        "    (<executable cli command>, <justification>) - APPROVED,"
        "  ]"
        "Suggestions in discussion: "
        "<agent> suggests:"
        "  [(<executable cli command>, <justification>), ...],"
        "  but is opposed by <agent> because <reason>, and suggests alternative:"
        "  [(<executable cli command>, <justification>), ...]"
        "..."
        "Suggest modification of disapproved actions or confirm approval."
        "```"
        
        "FINAL PROPOSALS FORMAT:"
        "Here are all approved suggestions of all agents:"
        "  ["
        "    (<agent>, <executable cli command>),"
        "    (<agent>, <executable cli command>),"
        "  ]"
        "..."
    )

def summarize_prompt(proposals: str) -> str:
    """
    Generates a prompt for summarizing agent responses in a multi-agent debate.

    This function constructs a prompt that guides the judge in summarizing
    the current state of the debate based on the received proposals. It also
    determines whether the debate should continue or end.

    Args:
        proposals (str): A string containing the agent proposals from the current round.

    Returns:
        str: A formatted prompt instructing how to summarize the proposals
             and decide if the debate should conclude.

    The prompt includes:
    - Instructions to determine the current debate round.
    - A request to summarize agent responses.
    - A condition to check whether all agents have agreed.
    - A directive to finalize and list the agreed-upon commands if consensus is reached.
    """
    return textwrap.dedent(
        "Calculate the round number and base on that summarize the following agent responses to the incoming attack: "
        f"{proposals}"
        "If the agents have agreed on all the commands, "
        "end the debate with 'THE DEBATE IS OVER' and write down all the commands that result from the debate."
    )