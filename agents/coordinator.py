from agents.agent import Agent


class Coordinator(Agent):
    def ask(self):
        response = self.send_llm('Jaké je průměrná teplota v lednu v Česku?')
        return response.msgs[0].content