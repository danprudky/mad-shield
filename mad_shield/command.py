from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agents import ComponentAgent


class Command:

    def __init__(self, component: "ComponentAgent", command: str) -> None:
        self.component = component
        self.command = command
