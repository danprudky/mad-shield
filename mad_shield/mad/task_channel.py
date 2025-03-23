from camel.societies.workforce.task_channel import TaskChannel as CamelTaskChannel, PacketStatus
from camel.tasks.task import Task

class TaskChannel(CamelTaskChannel):
    def __init__(self):
        super(TaskChannel, self).__init__()

    async def get_returned_task_by_assignee(self, assignee_id: str) -> Task:
        r"""Get a task from the channel that has been returned by the
        assignee.
        """
        async with self._condition:
            while True:
                for task_id in self._task_id_list:
                    packet = self._task_dict[task_id]
                    if packet.assignee_id != assignee_id:
                        continue
                    if packet.status != PacketStatus.RETURNED:
                        continue
                    return packet.task
                await self._condition.wait()