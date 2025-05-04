import os

from ..app_config import app_config
from ..mad.agents import LawyerAgent


class ComponentAgent:
    def __init__(self, info: tuple[str, list[str]]) -> None:
        component, paths = info
        self.name = component
        self.paths = paths
        self.description = self.__get_description()

    def __get_description(self) -> str:
        description = ""
        for path in self.paths:
            file_name = os.path.basename(path)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                description += f"{file_name}:\n{content}\n\n"
            except Exception as e:
                description += f"{file_name}: [Chyba při čtení: {e}]\n\n"

        return description

    from mad_shield.mad import MultiAgentDebate

    def hire_lawyer(self, mad: MultiAgentDebate) -> LawyerAgent:
        return LawyerAgent(self, mad)

    def execute(self, command: str) -> int:
        if app_config().not_execute_commands:
            print(self.name + " executing command: " + command)
            return 0
        print("Executing command: " + command)
        return os.system(command)
