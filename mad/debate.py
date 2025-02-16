from mad.agents import *
from configers import *
from .component import Component
from typing import List


class MultiAgentDebate:
    def __init__(self, max_rounds = 2) -> None:
        self.model = ModelLoader().load()
        self.max_rounds = max_rounds
        self.clients: List[ClientAgent] = []
        self.lawyers: List[LawyerAgent] = []

        for component in AgentLoader().load().items():
            client = ClientAgent(self, Component(component))
            self.clients.append(client)
            self.lawyers.append(client.lawyer)

        self.judge = JudgeAgent(self)

    def debate(self, alert) -> None:
        # TODO Implement
        print("Debating...")
        self.judge.init_debate(alert)

        debate_round = 1
        proposal_summary, is_over = self.judge.summarize_debate(debate_round)
        while not is_over and debate_round < self.max_rounds:
            debate_round += 1
            self.judge.get_opinion(debate_round)
            proposal_summary, is_over = self.judge.summarize_debate(debate_round)

        # Summarizer extern commands
        # TODO Implement
        executable_commands = [{
            'agent' : 'ssh_client',
            'commands' : ['ls', 'ls -h']
        }, {
            'agent' : 'firewall_client',
            'commands' : ['dir']
        }]

        for item in executable_commands:
            client_with_role = next((client for client in self.clients if client.role == item["agent"]), None)
            if client_with_role is not None:
                for command in item["commands"]:
                    client_with_role.execute(command)
            else:
                print(f"No client found with role: {item["agent"]}")