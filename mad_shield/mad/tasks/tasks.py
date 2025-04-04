from camel.tasks import Task

TASK_LAWYER_PROPOSE = Task(
        content="Analyze a current cyber attack, identify attack vectors and design specific "
                "executable CLI commands to mitigate the threat. Use your propose_prompt tool to do this.",
        type="Lawyer",
    )

TASK_SUMMARIZE = Task(
        content="Summarize all messages from lawyer agents in the current round in defined "
                "SUMMARIZATION FORMAT FOR {debate_round} ROUND PROPOSALS. Use your summarize_tool to do this.",
        type="Summarizer",
    )

TASK_LAWYER_CRITICIZE = Task(
    content="Provide a reaction to the proposals of all other agents in CRITICIZE FORMAT using react_prompt tool. "
            "Your goal is to review, critique, and, if necessary, refine the proposals made by other agents. "
            "Your responses should aim for a system-wide consensus while "
            "defending your component's interests.",
    type="Lawyer",
)

TASK_JUDGE_DEBATE = Task(
        content="Based on round summary evaluate whether all agents have approved all proposals. "
                "If another round of critique is requested, answer with 'DEBATE HAS TO CONTINUE'. "
                "If all proposals are approved, end the debate with FINAL PROPOSALS FORMAT "
                "as it is in your init message.",
        type="Judge",
    )

TASK_END_DEBATE = Task(
        content="Based on round summary evaluate whether all agents have approved all proposals. "
                "This is last debate round, pick all approved proposals and end the debate with FINAL PROPOSALS FORMAT "
                "as it is in your init message.",
        type="Judge",
    )