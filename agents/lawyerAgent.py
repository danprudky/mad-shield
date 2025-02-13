from agents.componentAgent import ComponentAgent


class LawyerAgent(ComponentAgent):
    def __init__(self, client, mad, component):
        super().__init__(mad, component)
        self.client = client
        self.init_msg = 'Budeš ' + component.component + ' agent'
        self.role = component.component + '_client'

    def hi(self):
        print('Hello, ' + self.role + ' here!')