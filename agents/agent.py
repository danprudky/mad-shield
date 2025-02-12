from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import BaseModelBackend
from camel.types import RoleType


class Agent:
    def __init__(self, model, init_msg):
        self.model: BaseModelBackend = model
        self.agent = ChatAgent(init_msg, model=model)

    def send_llm(self, msg):
        print('Sending llm message')
        user_message = BaseMessage(role_name="user", role_type=RoleType.USER, content=msg, meta_dict=None)
        return self.agent.step(user_message)