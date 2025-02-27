from abc import abstractmethod
from camel.agents import ChatAgent

from ...configers import PromptLoader, ModelLoader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mad_shield.mad.mad import MultiAgentDebate


class DebateAgent(ChatAgent):
    def __init__(
        self,
        mad: "MultiAgentDebate",
        role: str,
        prompt_file: str,
        model: str = "deepseek-r1",
    ) -> None:

        self.mad = mad
        self.model = ModelLoader(model).load()

        self.role: str = role
        self.prompts: dict[str, str] = PromptLoader(
            "mad_shield/config/prompts/" + prompt_file + ".yaml"
        ).load()

        super().__init__(system_message=self.get_init_msg(), model=self.model)

    @abstractmethod
    def get_init_msg(self) -> str:
        pass

    # def send_llm(self, msg):
    #    print('Sending llm message')
    #    user_message = BaseMessage(role_name="user", role_type=RoleType.USER, content=msg, meta_dict=None)
    #    return self.agent.step(user_message)
