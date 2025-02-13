from agents.debateAgent import DebateAgent


class JudgeAgent(DebateAgent):
    def __init__(self, mad):
        super().__init__(mad)
        for lawyer in mad.lawyers:
            lawyer.hi()

    #def ask(self):
    #    response = self.send_llm('Jaké je průměrná teplota v lednu v Česku?')
    #    return response.msgs[0].content