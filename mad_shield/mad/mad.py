import time
import ast

from typing import List
from typing import TYPE_CHECKING

from camel.tasks.task import Task

from .agents import *
from .agents.summarizer import SummarizerAgent
from mad_shield.mad.tasks.tasks import *
from .workforce import Workforce
from ..command import Command

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

        self.workforce.add_single_agent_worker(
            description="judge agent to decide if debate is over on end of each debate round",
            worker=self.judge,
        )

        self.workforce.load_children_data()

    def get_components_in_str(self) -> str:
        return ", ".join(component.name for component in self.components)

    def debate(self, alert: str) -> List[Command]:
        start = time.time()

        round_result = ""

        debate_round = 1
        is_consensus = False

        print("Max rounds: " + str(self.max_rounds))

        while not is_consensus and debate_round <= self.max_rounds:
            round_tasks: List[Task] = self.load_tasks(debate_round, alert)
            round_tasks = self._extend_lawyers_tasks(round_tasks)

            print(f"Having {len(round_tasks)} tasks for round {debate_round}")

            tasks = self.workforce.process_tasks(round_tasks)

            if debate_round <= 1:
                debate_round += 1
                continue

            round_result_task: Task = [task for task in tasks if self.workforce.get_task_assignee(task) == self.workforce.get_judge()][0]
            round_result = round_result_task.result

            is_consensus = True if "OVER" in round_result else False

            debate_round += 1

        print(f"\nDebating tasks: {time.time() - start} seconds")

        return self.parse_debate_result(round_result)

    def load_tasks(self, debate_round: int, alert: str) -> List[Task]:
        lawyers_task = TASK_LAWYER_PROPOSE if debate_round <= 1 else TASK_LAWYER_CRITICIZE
        summarizer_task = TASK_SUMMARIZE
        coordinator_task = TASK_JUDGE_DEBATE if debate_round < self.max_rounds else TASK_END_DEBATE

        if debate_round <= 1:
            lawyers_task.additional_info = f"Incoming alert: {alert}"
            summarizer_task.content = summarizer_task.content.format(debate_round='FIRST')
        else:
            summarizer_task.content = summarizer_task.content.format(debate_round='HIGHER')

        lawyers_task.id = f"{debate_round}.1"

        summarizer_task.id = f"{debate_round}.2"

        coordinator_task.id = f"{debate_round}.3"

        return [lawyers_task, summarizer_task] if debate_round <= 1 else [lawyers_task, summarizer_task, coordinator_task]

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

    def parse_debate_result(self, debate_result: str) -> list[Command]:
        """
        Parses the debate result and returns a list of Command objects.

        Args:
            debate_result (str): The debate output containing approved suggestions.

        Returns:
            list[Command]: A list of parsed commands assigned to their respective agents.
        """
        commands_list = []
        start = debate_result.find("[")
        end = debate_result.rfind("]")

        if start == -1 or end == -1:
            raise ValueError("Invalid debate result format.")

        cleaned_result = debate_result[start:end + 1]
        for lawyer in self.lawyers:
            cleaned_result = cleaned_result.replace(lawyer.role, f"'{lawyer.role}'")

        try:
            approved_commands = ast.literal_eval(cleaned_result)
        except (SyntaxError, ValueError) as e:
            raise ValueError(f"Error parsing debate result: {e}")

        for agent_name, command in approved_commands:
            lawyer_candidates = [agent for agent in self.lawyers if agent.role == agent_name]
            if len(lawyer_candidates) >= 1:
                commands_list.append(Command(lawyer_candidates[0].component, command))
            else:
                raise ValueError(f"Unknown agent: {agent_name}")

        return commands_list