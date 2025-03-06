from camel.tasks import Task


def debate_task(alert: str) -> Task:
    return Task(
        id="1",
        content="Multi-agent debate to secure system components against a cyber threat described in the incoming alert. The debate follows "
        "a structured process where a Judge agent coordinates the discussion among Lawyer agents, each representing a system component. "
        "Judge is coordinator of debate and every lawyer communicate only with him. "
        "Algorithm of debate has Judge described in his init message as DEBATE ALGORITHM."
        "Judge will use summary_prompt to summary proposals."
        "Lawyers will use propose_prompt in first round and then react_prompt.",
        additional_info=f"Incoming alert: {alert}",
    )
