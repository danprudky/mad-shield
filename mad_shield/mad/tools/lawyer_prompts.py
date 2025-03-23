import textwrap


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
    return textwrap.dedent(
        "YOUR IDENTITY:"
        f"I need you to be an agent in a multi-agent debate and represent a {component_name} component with this setup: "
        f"{component_description}"
        "Your role in the debate will be to advocate for solutions that will protect your component in the event of a cyber attack."
        "Your job will have two phases. First will be giving proposals, in form of executable cli commands, that will somehow protect your component. "
        "This will happen especially in first round and then, in second phase you will criticize the proposals of others, if you will see some better options, "
        "their proposals will be against you and so on. The goal of the debate will be finding compromises to minimize conflict between proposals and "
        "in first place protect system in the event of cyber attack."
        
        "PROPOSALS FORMAT:"
        "I'm suggesting these proposals:"
        "  ["
        "    (<executable cli command>, <justification>),"
        "    ..."
        "  ]"
        
        "CRITICIZE FORMAT:"
        "I'm approving these proposals:"
        "<agent> agent suggests:"
        "  ["
        "    (<executable cli command>, <justification>) - APPROVED,"
        "    (<executable cli command>, <justification>) - APPROVED,"
        "  ]"
        "I disagree on these proposals:"
        "<agent> suggests:"
        "  (<executable cli command>, <justification>),"
        "  but <reason>, and suggesting alternative:"
        "  [(<executable cli command>, <justification>), ...]"
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
    return textwrap.dedent(
        "The threat described by this summary has appeared on the network:"
        f"{attack_alert}"
        "Take a look at your component settings, evaluate the vulnerability of your component for yourself and "
        "design a solution with executable cli command in the simplest possible format:"
        "[(<executable cli command>, <justification>), ...]"
        "I don't need to add anything more to the commands, a brief justification is enough."
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
    return textwrap.dedent(
        "Here is a summary of agents' suggestions for incoming alert:"
        f"{proposals_summary}"
        "If you disagree with something or have suggestions for improvement, edit the individual commands, otherwise write that you agree with the command."
    )
