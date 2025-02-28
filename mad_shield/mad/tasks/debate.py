from camel.tasks import Task


def debate_task(alert: str, max_rounds: int) -> Task:
    task = Task(
        id="1",
        content="Multi-agent debate to secure system components against a cyber threat described in the incoming alert. The debate follows "
        "a structured process where a Judge agent coordinates the discussion among Lawyer agents, each representing a system component. "
        "Judge is coordinator of debate and every lawyer communicate only with him. "
        "Algorithm of debate has Judge described in judge_coordination_process",
        additional_info=f"Incoming alert: {alert}",
    )

    task.add_subtask(
        Task(
            id="1.1",
            content="The judge agent shares the incoming alert details with all lawyer agents.",
        )
    )

    task.add_subtask(
        Task(
            id="1.2",
            content="Lawyer agents analyze the alert and propose security measures for their respective components, providing "
            "executable CLI commands and justifications. This prompt is obtainable from the lawyer.propose_solution function.",
        )
    )

    task.add_subtask(
        Task(
            id="1.3",
            content="Judge agent summarizes the proposals from Lawyer agents and presents them for review.",
        )
    )

    task.add_subtask(
        Task(
            id="1.4",
            content="Lawyer agents review the summarized proposals and either agree or suggest modifications, providing reasons for any disagreements. "
            "This prompt is obtainable from the lawyer.react function.",
        )
    )

    task.add_subtask(
        Task(
            id="1.5",
            content="Judge agent consolidates responses and iterates the debate if needed, incorporating suggested modifications and ensuring consensus.",
        )
    )

    task.add_subtask(
        Task(
            id="1.6",
            content=f"Judge agent finalizes the debate if all agents agree or if the maximum number of rounds, which is {max_rounds}, is reached. "
            "The final set of approved security measures is documented.",
        )
    )

    return task
