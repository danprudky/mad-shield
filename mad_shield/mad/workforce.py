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