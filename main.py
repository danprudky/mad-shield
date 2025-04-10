import asyncio

from mad_shield import *


def main() -> None:
    mad_shield = MadShield("mad_shield/config/agents.yaml", 4)

    asyncio.run(mad_shield.defend("test/alert/sql_injection"))


if __name__ == "__main__":
    main()
