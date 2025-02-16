class Component:
    def __init__(self, info) -> None:
        component, paths = info
        self.component: str = component
        self.paths: list[str] = paths
