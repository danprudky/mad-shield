import asyncio

from mad_shield import MadShield

def main() -> None:
    config_path = "mad_shield/config/agents.yaml"
    max_debate_rounds = 4

    mad_shield = MadShield(config_path, max_debate_rounds)
    asyncio.run(mad_shield.run_service())

if __name__ == "__main__":
    main()