from configers.prompts import PromptLoader
from .componentAgent import ComponentAgent


class LawyerAgent(ComponentAgent):
    def __init__(self, client, mad, component) -> None:
        super().__init__(mad, component)

        from .clientAgent import ClientAgent

        self.client: ClientAgent = client
        self.role: str = component.name + "_lawyer"

        self.prompts: dict[str, str] = PromptLoader("config/prompts/lawyer.yaml").load()

        print(self.__get_init_msg())

    def __get_init_msg(self):
        return self.prompts["init"].format(
            component_name=self.component.name,
            component_description=self.component.description,
        )

    def __get_attack_msg(self, attack_alert: str):
        return self.prompts["attack"].format(attack_alert=attack_alert)

    def __get_react_msg(self, proposals_summary: str):
        return self.prompts["react"].format(proposals_summary=proposals_summary)

    def propose_solution(self, alert: str):
        msg = self.__get_attack_msg(alert)
        print(self.role + " proposing solution with:")
        print(msg)

    def react(self, debate_round: int) -> None:
        # Load message and create proposals or agree
        # TODO Implement
        msg = self.__get_react_msg("This is summary")
        print(
            self.role
            + " reacting on solution from round "
            + str(debate_round)
            + " with:"
        )
        print(msg)

    # TODO Delete
    def hi(self) -> None:
        print("Hello, " + self.role + " here!")
        print("Reading from:")
        for path in self.component.paths:
            print(path)
