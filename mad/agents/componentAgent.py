from .debateAgent import DebateAgent


class ComponentAgent(DebateAgent):
    def __init__(self, mad, component) -> None:
        super().__init__(mad)
        from ..component import Component

        self.component: Component = component
