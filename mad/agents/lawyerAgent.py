from .componentAgent import ComponentAgent


class LawyerAgent(ComponentAgent):
    def __init__(self, client, mad, component) -> None:
        super().__init__(mad, component)

        from .clientAgent import ClientAgent

        self.client: ClientAgent = client

        self.init_msg: str = "Budeš " + component.component + " agent"
        self.role: str = component.component + "_lawyer"

    def react(self, debate_round: int) -> None:
        # Load message and create proposals or agree
        # TODO Implement
        print(self.role + " reacting on solution from round " + str(debate_round) + "..")

    # TODO Delete
    def hi(self) -> None:
        print("Hello, " + self.role + " here!")
        print("Reading from:")
        for path in self.component.paths:
            print(path)