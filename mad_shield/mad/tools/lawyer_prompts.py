from camel.prompts import TextPrompt


def init_prompt(component_name: str, component_description: str) -> str:
    """
    Generates an initial prompt for an agent participating in a multi-agent debate.

    This function constructs a structured prompt that defines the role of an agent
    representing a specific system component in a debate focused on cyber attack protection.
    The agent is responsible for proposing solutions and evaluating the proposals of others.

    Args:
        component_name (str): The name of the component that the agent represents.
        component_description (str): A detailed description of the component's function and setup.

    Returns:
        str: A formatted prompt outlining the agent's responsibilities, debate structure,
             and required response formats.

    The prompt includes:
    - The agent's role and objectives in the debate.
    - Instructions for making protection proposals using CLI commands.
    - A second-phase role in analyzing and critiquing other agents' proposals.
    - A structured format for providing proposals and critiques.
    - The goal of the debate: finding compromises to protect the system while minimizing conflicts.
    """
    return TextPrompt(
        "YOUR IDENTITY:\n"
        f"I need you to be an agent in a multi-agent debate representing the {component_name} component with the following setup: {component_description}\n\n"
        "Your role is to propose defense strategies for your component in the event of a cyber attack. "
        "The debate will have two distinct phases:\n"
        "1. In the first round, provide your proposals as executable CLI commands with brief justifications using propose_tool.\n"
        "2. Starting from the second round, respond to other agents’ proposals using the react_prompt tool and format it into CRITICIZE FORMAT. "
        "Every response from you must strictly follow the CRITICIZE FORMAT from round 2 onward.\n\n"
        
        "PROPOSALS FORMAT:\n"
        "I'm suggesting these proposals:\n"
        "  [\n"
        "    (<executable cli command>, <justification>),\n"
        "    ...\n"
        "  ]\n\n"
        
        "CRITICIZE FORMAT:\n"
        "I'm approving these proposals:\n"
        "<agent> agent suggests:\n"
        "  [\n"
        "    (<executable cli command>, <justification>) - APPROVED,\n"
        "    ...\n"
        "  ]\n"
        "I disagree on these proposals:\n"
        "<agent> suggests:\n"
        "  (<executable cli command>, <justification>),\n"
        "  because <reason>, and suggesting alternative:\n"
        "  [ (<executable cli command>, <justification>), ... ]\n"
        "..."
    )


def propose_prompt(attack_alert: str) -> str:
    """
    Generates a prompt for an agent to propose a defense strategy against a cyberattack.

    This function constructs a structured prompt that instructs an agent to analyze
    a given attack alert and propose a defense mechanism in the form of executable
    CLI commands.

    Args:
        attack_alert (str): A description of the detected cyber threat.

    Returns:
        str: A formatted prompt instructing the agent to evaluate its component’s
             vulnerabilities and propose protective measures.

    The prompt includes:
    - A summary of the detected threat.
    - A request for the agent to assess its component’s vulnerability.
    - Instructions to generate a solution using executable CLI commands.
    - A requirement for brief justifications alongside the proposed commands.
    """
    return TextPrompt(
        "The threat described by this summary has appeared on the network:\n"
        f"{attack_alert}\n"
        "Review your component settings, evaluate the vulnerability, and design a solution with executable CLI commands in the simplest possible format:\n"
        "  [ (<executable cli command>, <justification>), ... ]\n"
        "Provide a brief justification for each command."
    )


def react_prompt(proposals_summary: str) -> str:
    """
    Generates a prompt for an agent to respond to summarized proposals in a multi-agent debate.

    This function constructs a structured prompt that presents a summary of previously
    suggested defensive actions and asks the agent to review, approve, or suggest modifications.

    Args:
        proposals_summary (str): A summary of proposals from other agents regarding
                                 the incoming cyber threat.

    Returns:
        str: A formatted prompt instructing the agent to evaluate the proposals,
             either approving them or suggesting improvements.

    The prompt includes:
    - A summary of the proposed actions.
    - A request for the agent to review and provide feedback.
    - Instructions to either approve the commands or suggest modifications.
    """
    return TextPrompt(
        "Here is a summary of lawyer agents' suggestions for the incoming alert:\n"
        f"{proposals_summary}\n"
        "Starting from the second round, please review the proposals and respond in CRITICIZE FORMAT. "
        "If you agree with a command, simply state your approval. If not, provide your critique and propose an alternative."
    )
