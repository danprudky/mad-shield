import argparse
import asyncio

from mad_shield import MadShield

def parse_args():
    parser = argparse.ArgumentParser(description="Run multi-agent debate shield.")

    parser.add_argument(
        "--max-debate-rounds",
        type=int,
        default=4,
        help="Maximum number of debate rounds.",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    config_path = "mad_shield/config/agents.yaml"

    mad_shield = MadShield(config_path, args.max_debate_rounds)
    asyncio.run(mad_shield.run_service())

if __name__ == "__main__":
    main()