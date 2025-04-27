from abc import abstractmethod
from camel.agents import ChatAgent
from camel.messages import BaseMessage

from ...configers import ModelLoader
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..mad import MultiAgentDebate
    from camel.models import BaseModelBackend


class DebateAgent(ChatAgent):
    def __init__(self, mad: "MultiAgentDebate", role: str, **kwargs: Any) -> None:

        self.mad: "MultiAgentDebate" = mad
        self.model: "BaseModelBackend" = ModelLoader().load_model()

        self.role: str = role

        sys_msg = BaseMessage.make_assistant_message(
            role_name=self.role, content=self.get_init_msg()
        )

        super().__init__(system_message=sys_msg, model=self.model, **kwargs)

    @abstractmethod
    def get_init_msg(self) -> str:
        pass

    def sent_prompt(self, prompt: str) -> str:
        response = self.step(prompt)
        return response.msgs[0].content
