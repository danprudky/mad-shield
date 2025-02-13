from agents.debateAgent import DebateAgent


class ComponentAgent(DebateAgent):
    def __init__(self, mad, component):
        super().__init__(mad)
        self.component = component