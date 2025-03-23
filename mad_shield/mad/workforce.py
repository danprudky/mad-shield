import asyncio
from typing import List

from camel.societies.workforce import Workforce as CamelWorkforce
from camel.societies.workforce.task_channel import TaskChannel
from camel.tasks.task import Task, TaskState


class Workforce(CamelWorkforce):
    def __init__(self, coordinator = None, **kwargs):
        super(Workforce, self).__init__(**kwargs)

        self._summarizer_id = None
        self._lawyers_ids = None

        if coordinator is not None:
            self.coordinator_agent = coordinator

    def load_children_data(self):
        self._lawyers_ids = self.get_lawyers_node_ids()
        self._summarizer_id = self.get_summarizer_node_id()

    def process_tasks(self, tasks: List[Task]) -> Task:
        self.reset()

        self._pending_tasks.extendleft(reversed(tasks))
        self.set_channel(TaskChannel())

        asyncio.run(self.start())

        return tasks[0]

    def get_lawyers_node_ids(self) -> List[int]:
        return [child.node_id for child in self._children if "lawyer" in child.worker.role_name]

    def get_summarizer_node_id(self) -> int:
        ids = [child.node_id for child in self._children if "summarizer" in child.worker.role_name]
        return ids[0]

    async def _post_ready_tasks(self) -> None:
        if not self._pending_tasks:
            return

        ready_task = self._pending_tasks[0]
        print(ready_task.state)

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
                for assignee_id in self._lawyers_ids:
                    await self._post_task(ready_task, str(assignee_id))
            elif ready_task.type == "Summarizer":
                await self._post_task(ready_task, str(self._summarizer_id))
            else:
                await self._post_task(ready_task, str(self.coordinator_agent.node_id))