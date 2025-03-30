import asyncio
import logging

from typing import List
from colorama import Fore

from camel.societies.workforce import Workforce as CamelWorkforce
from camel.societies.workforce.base import BaseNode
from camel.tasks.task import Task, TaskState

from .task_channel import TaskChannel

logger = logging.getLogger(__name__)

class Workforce(CamelWorkforce):
    def __init__(self, **kwargs):
        super(Workforce, self).__init__(**kwargs)

        self._lawyers = None
        self._summarizer = None
        self._judge = None
        self._tasks_in_progress: List[Task] = []
        self._debate_channel: TaskChannel = TaskChannel()

    def load_children_data(self):
        self._lawyers = self.get_lawyer_nodes()
        self._summarizer = self.get_summarizer_node()
        self._judge = self.get_judge_node()

    def process_tasks(self, tasks: List[Task]) -> List[Task]:
        self.reset()

        self._pending_tasks.extendleft(reversed(tasks))

        self.set_channel(self._debate_channel)

        if not self._debate_channel.get_loop().is_running():
            self._debate_channel.get_loop().run_until_complete(self.start())
        else:
            asyncio.ensure_future(self.start())

        return tasks

    def get_lawyers(self) -> List[BaseNode]:
        return self._lawyers

    def get_summarizer(self) -> BaseNode:
        return self._summarizer

    def get_judge(self) -> BaseNode:
        return self._judge

    def get_lawyer_nodes(self) -> List[BaseNode]:
        return [child for child in self._children if "lawyer" in child.worker.role_name]

    def get_summarizer_node(self) -> BaseNode:
        return [child for child in self._children if "summarizer" in child.worker.role_name][0]

    def get_judge_node(self):
        return [child for child in self._children if "judge" in child.worker.role_name][0]

    async def _post_task(self, task: Task, assignee: BaseNode) -> None:
        await self._channel.post_task(task, self.node_id, assignee.node_id)

    async def _post_dependency(self, dependency: Task) -> None:
        await self._channel.post_dependency(dependency, self.node_id)

    async def _get_returned_task_from_assignee(self, assignee: BaseNode) -> Task:
        r"""Get the task that's published by this node and just get returned
        from the assignee.
        """
        return await self._channel.get_returned_task_by_assignee(assignee.node_id)  #TODO: Dotypovvat

    async def _post_ready_tasks(self) -> None:
        if not self._pending_tasks:
            return

        ready_task = self._pending_tasks[0]

        self._tasks_in_progress.append(ready_task)

        # If the task has failed previously, just compose and send the task
        # to the channel as a dependency
        if ready_task.state == TaskState.FAILED:
            self.task_agent.reset()
            # Remove the subtasks from the channel
            for subtask in ready_task.subtasks:
                await self._channel.remove_task(subtask.id)
            # Send the task to the channel as a dependency
            await self._post_dependency(ready_task)
            self._pending_tasks.popleft()
            # Try to send the next task in the pending list
            await self._post_ready_tasks()
        else:
            # Directly post the task to the channel if it's a new one
            # Find a node to assign the task
            self._working_assignee = self.get_task_assignee(ready_task)
            await self._post_task(ready_task, self._working_assignee)

    async def _listen_to_channel(self) -> None:
        self._running = True

        while len(self._pending_tasks) > 0:
            await self._post_ready_tasks()
            returned_task = self._tasks_in_progress.pop()
            await self._get_returned_task_from_assignee(self._working_assignee)

            if returned_task.state == TaskState.DONE:
                await self._handle_completed_task(returned_task)
            elif returned_task.state == TaskState.FAILED:
                halt = await self._handle_failed_task(returned_task)
                if not halt:
                    continue
                self.stop()
                print(
                    f"{Fore.RED}Task {returned_task.id} has failed "
                    f"for 3 times, halting the workforce.{Fore.RESET}"
                )
                break
            elif returned_task.state == TaskState.OPEN:
                # TODO: multi-layer workforce
                pass
            else:
                raise ValueError(
                    f"Task {returned_task.id} has an unexpected state."
                )

        self.stop()

    async def _handle_completed_task(self, task: Task) -> None:
        # archive the packet, making it into a dependency
        self._pending_tasks.popleft()
        await self._channel.archive_task(task.id)

    def get_task_assignee(self, task: Task) -> BaseNode:
        if task.type == "Lawyer":
            assignee_id = task.id.split(".")[2]
            assignee = next((a for a in self._lawyers if a.node_id == assignee_id), None)
            return assignee
        elif task.type == "Summarizer":
            return self._summarizer
        else:
            return self._judge