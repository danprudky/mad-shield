import os


class Component:
    def __init__(self, info) -> None:
        component, paths = info
        self.name: str = component
        self.paths: list[str] = paths
        self.description: str = self.__get_description()

    def __get_description(self):
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
