from abc import abstractmethod
from camel.agents import ChatAgent
from camel.messages import BaseMessage

from ...configers import PromptLoader, ModelLoader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate


class DebateAgent(ChatAgent):  # type: ignore
    def __init__(self, mad: "MultiAgentDebate", role: str, prompt_file: str) -> None:

        self.mad = mad
        self.model = ModelLoader().gpt_4o_mini()

        self.role: str = role
        self.prompts: dict[str, str] = PromptLoader(
            "mad_shield/config/prompts/" + prompt_file + ".yaml"
        ).load()

        sys_msg = BaseMessage.make_assistant_message(
            role_name=self.role, content=self.get_init_msg()
        )

        super().__init__(system_message=sys_msg, model=self.model)

    @abstractmethod
    def get_init_msg(self) -> str:
        pass
