import time

from typing import List
from typing import TYPE_CHECKING

from camel.tasks.task import Task

from .agents import *
from mad_shield.mad.tasks.debate import debate_task
from .agents.summarizer import SummarizerAgent
from mad_shield.mad.tasks.debate import TASK1, TASK2, TASK3, TASK4, TASK5, TASK6
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


        task = self.workforce.process_tasks(self.load_tasks())

        print(f"\nDebating tasks: {time.time() - start} seconds")
        print(task.result)

    @staticmethod
    def load_tasks() -> List[Task]:
        return [TASK1, TASK2, TASK3, TASK4, TASK5, TASK6]

    def task_test(self, alert: str) -> None:
        task = debate_task(alert, 3)

        new_tasks = task.decompose(agent=self.judge)
        for t in new_tasks:
            print(t.to_string())

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