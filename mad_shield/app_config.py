class AppConfig:
    _instance = None
    max_debate_rounds: int
    polling_interval: int
    debug: bool
    not_execute_commands: bool
    process_one: bool

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.max_debate_rounds = 4
            cls._instance.debug = False
            cls._instance.not_execute_commands = False
            cls._instance.process_one = False
        return cls._instance

    def set_values(self,
                   max_debate_rounds: int,
                   polling_interval: int,
                   debug: bool = False,
                   not_execute_commands: bool = False,
                   process_one: bool = False
                   ) -> None:
        self.max_debate_rounds = max_debate_rounds
        self.polling_interval = polling_interval
        self.debug = debug
        self.not_execute_commands = not_execute_commands
        self.process_one = process_one


def app_config() -> AppConfig:
    return AppConfig()