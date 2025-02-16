class DebateAgent:
    def __init__(self, mad) -> None:
        from ..debate import MultiAgentDebate

        self.mad: MultiAgentDebate = mad
        self.model = self.mad.model
        # self.agent = ChatAgent(init_msg, model=self.model)

    # def send_llm(self, msg):
    #    print('Sending llm message')
    #    user_message = BaseMessage(role_name="user", role_type=RoleType.USER, content=msg, meta_dict=None)
    #    return self.agent.step(user_message)
