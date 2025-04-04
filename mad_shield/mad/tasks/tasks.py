from camel.tasks import Task

TASK_LAWYER_PROPOSE = Task(
        content="Write me your secure suggestions as executable CLI commands, using proposal_prompt tool.",
        type="Lawyer",
    )

TASK_SUMMARIZE = Task(
        content="Summarize all messages from lawyer agents in the current round in defined "
                "SUMMARIZATION FORMAT FOR {debate_round} ROUND PROPOSALS. Use your summarize_tool to do this.",
        type="Summarizer",
    )

TASK_LAWYER_CRITICIZE = Task(
        content="Provide a reaction to the proposals of all other agents in CRITICIZE FORMAT using react_prompt tool.",
        type="Lawyer",
    )

TASK_END_DEBATE = Task(
        content="Based on round summary evaluate whether all agents have approved all proposals. "
                "If not and maximum round is not reached, another round of critique is requested, answer with "
                "'DEBATE HAS TO CONTINUE'. "
                "If the debate has reached {max_rounds} rounds, or all proposals are approved, "
                "the debate is ended with FINAL PROPOSALS FORMAT as it is in your init message.",
        type="Coordinator",
    )