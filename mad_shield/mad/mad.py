import time

from typing import List
from typing import TYPE_CHECKING

from camel.tasks.task import Task

from .agents import *
from .agents.summarizer import SummarizerAgent
from mad_shield.mad.tasks.tasks import TASK_LAWYER_PROPOSE, TASK_SUMMARIZE, TASK_LAWYER_CRITICIZE
from .workforce import Workforce

if TYPE_CHECKING:
    from mad_shield.agents.componentAgent import ComponentAgent


class MultiAgentDebate:
    def __init__(self, components: List["ComponentAgent"], max_rounds: int = 5) -> None:
        self.max_rounds = max_rounds
        self.components = components

        self.lawyers: List[LawyerAgent] = []
        self.summarizer = None
        self.judge = None
        self.workforce = None

    def load_agents(self):
        for component in self.components:
            self.lawyers.append(component.hire_lawyer(self))

        self.summarizer = SummarizerAgent(self)
        self.judge = JudgeAgent(self)

    def load_workforce(self):
        self.workforce = Workforce(
            coordinator=self.judge,
            description="Multiagent debate shield"
        )

        for lawyer in self.lawyers:
            self.workforce.add_single_agent_worker(
                description=lawyer.role + " is component agent defending his component",
                worker=lawyer,
            )

        self.workforce.add_single_agent_worker(
            description="summarizer agent to condense and extract proposals from each debate round",
            worker=self.summarizer,
        )

        self.workforce.load_children_data()

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)

    def debate(self, alert: str) -> None:
        start = time.time()

        debate_round = 1
        is_consensus = False

        print("Max rounds: " + str(self.max_rounds))

        while not is_consensus and debate_round <= self.max_rounds:
            round_tasks: List[Task] = self.load_tasks(debate_round, alert)
            round_tasks = self._extend_lawyers_tasks(round_tasks)
            print(f"Having {len(round_tasks)} tasks for round {debate_round}")
            tasks = self.workforce.process_tasks(round_tasks)
            round_result_task: Task = [task for task in tasks if self.workforce.get_task_assignee(task) == self.workforce.get_summarizer()][0]
            print(round_result_task.result)
            debate_round += 1

        print(f"\nDebating tasks: {time.time() - start} seconds")

    @staticmethod
    def load_tasks(debate_round: int, alert: str) -> List[Task]:
        lawyers_task = TASK_LAWYER_PROPOSE if debate_round == 1 else TASK_LAWYER_CRITICIZE
        summarizer_task = TASK_SUMMARIZE

        if debate_round == 1:
            lawyers_task.additional_info = f"Incoming alert: {alert}"
            summarizer_task.content = summarizer_task.content.format(debate_round='FIRST')
        else:
            summarizer_task.content = summarizer_task.content.format(debate_round='HIGHER')

        print(summarizer_task.content)

        lawyers_task.id = f"{debate_round}.1"

        summarizer_task.id = f"{debate_round}.2"

        return [lawyers_task, summarizer_task]

    def _extend_lawyers_tasks(self, tasks: List[Task]) -> List[Task]:
        lawyer_tasks = [task for task in tasks if task.type == "Lawyer"]
        for task in lawyer_tasks:
            task_index = tasks.index(task)
            tasks.remove(task)

            for assignee in self.workforce.get_lawyers():
                lawyer_task = task.model_copy()
                lawyer_task.id = task.id + "." + assignee.node_id
                tasks.insert(task_index, lawyer_task)
                task_index += 1
        return tasks

#        # Summarizer extern commands
#        # TODO Implement
#        executable_commands = [
#            ["ssh", "ls -h"],
#            ["ssh", "ls"],
#            ["firewall", "dir"],
#        ]
#
#        result = []
#        for component, command in executable_commands:
#            c = next((c for c in self.components if c.name == component), None)
#            if c is None:
#                raise ValueError(f"Component '{component}' not found")
#            result.append(Command(c, command))
#        return result