from agents.clientAgent import ClientAgent
from agents.judgeAgent import JudgeAgent
from component import Component
from config_loader import ConfigLoader


class MAD:
    def __init__(self):
        self.model = ConfigLoader().get_model()
        self.clients: list = []
        self.lawyers: list = []

        for component in ConfigLoader().get_agents().items():
            client = ClientAgent(self, Component(component))
            client.hire_lawyer()
            self.clients.append(client)
            self.lawyers.append(client.lawyer)

        JudgeAgent(self)


    def debate(self, alert):
        print('Debating...')