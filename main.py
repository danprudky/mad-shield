import logging

from mad_shield import *


def main() -> None:
    logging.basicConfig(
        filename='mad.log',
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )

    mad_shield = MadShield("mad_shield/config/agents.yaml", 1)

    mad_shield.go("test/alert/sql_injection")


if __name__ == "__main__":
    main()