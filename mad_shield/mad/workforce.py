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
    def __init__(self, coordinator = None, **kwargs):
        super(Workforce, self).__init__(**kwargs)

        self._lawyers = None
        self._summarizer = None
        self._task_in_progress = None

        if coordinator is not None:
            self.coordinator_agent = coordinator

    def load_children_data(self):
        self._lawyers = self.get_lawyer_nodes()
        self._summarizer = self.get_summarizer_node()

    def process_tasks(self, tasks: List[Task]) -> Task:
        self.reset()

        self._pending_tasks.extendleft(reversed(tasks)) #TODO: Možná bude potřeba ladit task id, třeba to nechodí kvůli tomu
        self.set_channel(TaskChannel())

        asyncio.run(self.start())

        return tasks[0]

    def get_lawyer_nodes(self) -> List[BaseNode]:
        return [child for child in self._children if "lawyer" in child.worker.role_name]

    def get_summarizer_node(self) -> BaseNode:
        return [child for child in self._children if "summarizer" in child.worker.role_name][0]

    async def _post_task(self, task: Task, assignee: BaseNode) -> None:
        logger.info(f"Posting task to \"{assignee.worker.role_name}\"") #TODO: DAN SMAZAT
        task.id = task.id + "." + str(int(assignee.node_id) % 100000)   #TODO: Toto nejde, každý musí mít svůj task
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
        self._task_in_progress = ready_task
        logger.info(f"Task \"{ready_task.content}\" getting posted.")

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
            if ready_task.type == "Lawyer":
                for assignee in self._lawyers:
                    await self._post_task(ready_task, assignee)
            elif ready_task.type == "Summarizer":
                await self._post_task(ready_task, self._summarizer)
            else:
                await self._post_task(ready_task, self)

    async def _listen_to_channel(self) -> None:
        self._running = True
        logger.info(f"Workforce {self.node_id} started.")

        await self._post_ready_tasks()

        logger.info(f"Workforce {self.node_id} await done.")

        while self._task_in_progress is not None or self._pending_tasks:
            if self._task_in_progress.type == "Lawyer":
                returned_tasks = []
                for assignee in self._lawyers:
                    returned_task = await self._get_returned_task_from_assignee(assignee)
                    returned_tasks.append(returned_task)
            elif self._task_in_progress.type == "Summarizer":
                returned_tasks = [await self._get_returned_task_from_assignee(self._summarizer)]
            else:
                returned_tasks = [await self._get_returned_task_from_assignee(self)]

            for returned_task in returned_tasks:
                if returned_task.state == TaskState.DONE:
                    await self._handle_completed_task(returned_task)
                elif returned_task.state == TaskState.FAILED:
                    halt = await self._handle_failed_task(returned_task)
                    if not halt:
                        continue
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

        # shut down the whole workforce tree
        self.stop()