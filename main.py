import asyncio
import logging
import textwrap

from mad_shield import *


def main() -> None:
    mad_shield = MadShield("mad_shield/config/agents.yaml", 2)

    asyncio.run(mad_shield.go("test/alert/sql_injection"))


if __name__ == "__main__":
    main()