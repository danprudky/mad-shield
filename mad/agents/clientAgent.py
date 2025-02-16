from .componentAgent import ComponentAgent
from .lawyerAgent import LawyerAgent


class ClientAgent(ComponentAgent):
    def __init__(self, mad, component) -> None:
        super().__init__(mad, component)
        self.init_msg: str = "Budeš " + component.name + " agent"
        self.role: str = component.name + "_client"
        self.lawyer: LawyerAgent = self.hire_lawyer()

    def hire_lawyer(self) -> LawyerAgent:
        return LawyerAgent(self, self.mad, self.component)

    def execute(self, command: str) -> None:
        # TODO Implement
        print(f"{self.role} running command: {command}")

    # TODO Delete
    def hi(self) -> None:
        print("Hello, " + self.role + " here!")
