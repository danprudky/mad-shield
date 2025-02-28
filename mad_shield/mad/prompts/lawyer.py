import textwrap


def init_prompt(component_name: str, component_description: str) -> str:
    return textwrap.dedent(
        f"I need you to be an agent in a multi-agent debate and represent a {component_name} component with this setup: "
        f"{component_description}"
        "Your role in the debate will be to advocate for solutions that will protect your component in the event of a cyber attack, "
        "criticizing the proposals of others, and finding compromises to minimize conflict."
        "Do not respond to this message and just get into character."
    )


def propose_prompt(attack_alert: str) -> str:
    # return self.prompts["attack"].format(attack_alert=attack_alert)
    return textwrap.dedent(
        "The threat described by this summary has appeared on the network:"
        f"{attack_alert}"
        "Take a look at your component settings, evaluate the vulnerability of your component for yourself and "
        "design a solution with executable cli command in the simplest possible format:"
        "[(<executable cli command>, <justification>), ...]"
        "I don't need to add anything more to the commands, a brief justification is enough."
    )


def react_prompt(proposals_summary: str) -> str:
    return textwrap.dedent(
        "Here is a summary of agents' suggestions for incoming alert:"
        f"{proposals_summary}"
        "If you disagree with something or have suggestions for improvement, edit the individual commands, otherwise write that you agree with the command."
    )
