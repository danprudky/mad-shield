from camel.tasks import Task


def debate_task(alert: str, max_rounds: int) -> Task:
    task = Task(
        id="1",
        content="Multi-agent debate to secure system components against a cyber threat described in the incoming alert. The debate follows "
        "a structured process where a Judge agent coordinates the discussion among Lawyer agents, each representing a system component, "
        "and Summarizer agent to structure each round output. "
        "Judge is coordinator of debate and every lawyer communicate only with him. "
        "Summarizer will use summary_prompt to summary proposals. "
        "Lawyers will use propose_prompt in first round and then react_prompt. "

        "DEBATE ALGORITHM:\n"
        "1. Each lawyer agent asynchronously proposes secure suggestions as executable CLI commands.\n"
        "2. After the each round, each lawyer agent has to be requested by coordinator to provide a reaction to the all proposals of other agents in CRITICIZE FORMAT.\n"
        "3. The summarizer agent will only aggregate the proposals and reactions, but will NOT drive or lead the debate.\n"
        "4. In every round, after collecting responses, check if all agents have approved all proposals. If so, or if the maximum round count reaches "
        f"{max_rounds}, you must end the debate.\n"
        "5. When ending the debate, output the final data strictly in the FINAL PROPOSALS FORMAT below (this format must be maintained for subsequent parsing).\n\n",
        additional_info=f"Incoming alert: {alert}",
        result="FINAL PROPOSALS FORMAT:\n"
               "Here are all approved suggestions of all agents:\n"
               "  [\n"
               "    (<agent>, <executable cli command>),\n"
               "    (<agent>, <executable cli command>),\n"
               "  ]\n"
               "...",
    )

    #task.add_subtask(
    #    Task(
    #        id="1.2",
    #        content="Summarizer agent summarize all proposals, with summarize_prompt tool and given SUMMARY FORMATS. "
    #                "Give them back to the coordinator."
    #    )
    #)
#
    #task.add_subtask(
    #    Task(
    #        id="1.1",
    #        content="Coordinator agent ask asynchronously all lawyer agents for their secure suggestions proposes, as "
    #                "executable CLI commands, using proposal_prompt tool. They send their proposals back to coordinator.",
    #    )
    #)
#
    #task.add_subtask(
    #    Task(
    #        id="1.3",
    #        content="Coordinator agent ask asynchronously all lawyers for reaction on all other agents proposals. They should "
    #                "generate reply using react_prompt tool."
    #    )
    #)
#
    #task.add_subtask(
    #    Task(
    #        id="1.4",
    #        content="Repeat subtasks 1.2 and then if judge(coordinator) can declare the debate over return results in judge's FINAL PROPOSALS FORMAT."
    #    )
    #)

    return task

TASK1 = Task(
        id="1.1",
        content="Write me your secure suggestions as executable CLI commands, using proposal_prompt tool.",
        type="Lawyer",
        additional_info="Incoming alert: {alert}",
    )

TASK2 = Task(
        id="1.2",
        content="Aggregates all received proposals from recently finished workforce tasks and formats them using summary_prompt.",
        type="Summarizer",
    )

TASK3 = Task(
        id="2.1",
        content="Provide a reaction to the proposals of all other agents in CRITICIZE FORMAT using react_prompt tool.",
        type="Lawyer",
    )

TASK4 = Task(
        id="2.2",
        content="Aggregates all received proposals and formats them using summary_prompt.",
        type="Summarizer",
    )

TASK5 = Task(
        id="2.3",
        content="Coordinator agent evaluates whether all agents have approved all proposals. "
                "If not, another round of critique is requested (repeat subtasks of 2). "
                "If the debate has reached {max_rounds} rounds, or all proposals are approved, the debate is ended with FINAL PROPOSALS FORMAT."
                
                "FINAL PROPOSALS FORMAT:\n"
                "DEBATE IS OVER!\n"
                "Here are all approved suggestions of all agents:\n"
                "  [\n"
                "    (<agent>, <executable cli command>),\n"
                "    (<agent>, <executable cli command>),\n"
                "  ]\n"
                "...",
        type="Coordinator",
    )

TASK6 = Task(
        id="3",
        content="If all proposals have been approved or the maximum round count has been reached, "
                "Coordinator agent outputs the final data strictly in the FINAL PROPOSALS FORMAT below."
                
                "FINAL PROPOSALS FORMAT:\n"
                "DEBATE IS OVER!\n"
                "Here are all approved suggestions of all agents:\n"
                "  [\n"
                "    (<agent>, <executable cli command>),\n"
                "    (<agent>, <executable cli command>),\n"
                "  ]\n"
                "...",
        type="Coordinator",
    )
