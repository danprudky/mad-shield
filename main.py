from mad_shield import *


def main() -> None:
    mad_shield = MadShield("mad_shield/config/agents.yaml", 3)

    mad_shield.go("test/alert/sql_injection")


if __name__ == "__main__":
    main()