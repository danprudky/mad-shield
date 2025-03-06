from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.societies.workforce import Workforce as CamelWorkforce
from camel.types import ModelPlatformType, ModelType


class Workforce(CamelWorkforce):
    def __init__(self, coordinator = None, **kwargs):
        super(Workforce, self).__init__(**kwargs)

        if coordinator is not None:
            self.coordinator_agent = coordinator

    #def _create_new_agent(self, role: str, sys_msg: str) -> ChatAgent:
    #    worker_sys_msg = BaseMessage.make_assistant_message(
    #        role_name=role,
    #        content=sys_msg,
    #    )
#
    #    if self.new_worker_agent_kwargs is not None:
    #        return ChatAgent(worker_sys_msg, **self.new_worker_agent_kwargs)
#
    #    # Default tools for a new agent
    #    function_list = [
    #        #
    #    ]
#
    #    model_config_dict = ChatGPTConfig(
    #        tools=function_list,
    #        temperature=0.0,
    #    ).as_dict()
#
    #    model = ModelFactory.create(
    #        model_platform=ModelPlatformType.DEFAULT,
    #        model_type=ModelType.DEFAULT,
    #        model_config_dict=model_config_dict,
    #    )
#
    #    return ChatAgent(worker_sys_msg, model=model, tools=function_list)  # type: ignore[arg-type]