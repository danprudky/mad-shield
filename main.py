import argparse
import asyncio

from mad_shield import MadShield
from mad_shield.app_config import app_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-agent debate shield.")

    parser.add_argument(
        "--max-debate-rounds",
        type=int,
        default=4,
        help="Maximum number of debate rounds.",
    )

    parser.add_argument(
        "--polling-interval",
        type=int,
        default=3,
        help="Number of seconds to wait between alert polls.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Used for testing, enable debug printing.",
    )

    parser.add_argument(
        "--not-execute-commands",
        action="store_true",
        help="Used for testing, it disables executing commands.",
    )

    parser.add_argument(
        "--process-one",
        action="store_true",
        help="Used for testing, it just process one alert and exit.",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    app_config().set_values(
        args.max_debate_rounds,
        args.polling_interval,
        args.debug,
        args.not_execute_commands,
        args.process_one
    )

    config_path = "mad_shield/config/agents.yaml"

    mad_shield = MadShield(config_path)
    asyncio.run(mad_shield.run_service())

if __name__ == "__main__":
    main()