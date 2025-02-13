from agents.componentAgent import ComponentAgent
from agents.lawyerAgent import LawyerAgent


class ClientAgent(ComponentAgent):
    def __init__(self, mad, component):
        super().__init__(mad, component)
        self.lawyer = None
        self.init_msg = 'Budeš ' + component.component + ' agent'
        self.role = component.component + '_client'

    def hire_lawyer(self):
        self.lawyer = LawyerAgent(self, self.mad, self.component)

    def hi(self):
        print('Hello, ' + self.role + ' here!')