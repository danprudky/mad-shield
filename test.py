import subprocess
import time
import csv
import os

from dotenv import load_dotenv
from datetime import date

import requests

OUTPUT_FILE = "benchmark_results.csv"
RUNS_PER_ROUND = 3
ROUND_VALUES = range(2, 5)  # 2 až 5

def get_token_usage():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {'Authorization': f'Bearer {api_key}'}
    url = 'https://api.openai.com/v1/usage'
    params = {'date': date.today().strftime('%Y-%m-%d')}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_token_stats():
    usage_data = get_token_usage()
    total_input_tokens = 0
    total_output_tokens = 0

    for entry in usage_data.get("data", []):
        total_input_tokens += entry.get("n_context_tokens_total", 0)
        total_output_tokens += entry.get("n_generated_tokens_total", 0)

    return total_input_tokens, total_output_tokens

def run_once(max_rounds):
    start_time = time.time()

    start_input_tokens, start_output_tokens = get_token_stats()

    result = subprocess.run([
            "python3.12",
            "main.py",
            "--max-debate-rounds", str(max_rounds),
            "--debug",
            "--not-execute-commands",
            "--process-one"
        ],
        capture_output=True,
        text=True
    )

    duration = time.time() - start_time

    with open(f"test/test_{max_rounds}_{start_time}", "w") as f:
        f.write(result.stdout)
        f.write("\n--- STDERR ---\n")
        f.write(result.stderr)

    end_input_tokens, end_output_tokens = get_token_stats()

    return {
        "max_rounds": max_rounds,
        "duration_sec": round(duration, 2),
        "prompt_tokens": end_input_tokens - start_input_tokens,
        "completion_tokens": end_output_tokens - start_output_tokens,
        "success": result.returncode == 0,
        "stderr": result.stderr.strip() if result.returncode != 0 else ""
    }

def main():
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "max_rounds", "duration_sec",
            "prompt_tokens", "completion_tokens",
            "success", "stderr"
        ])
        writer.writeheader()

        for max_rounds in ROUND_VALUES:
            for i in range(RUNS_PER_ROUND):
                print(f"Spouštím test {i+1}/{RUNS_PER_ROUND} pro max_rounds={max_rounds} ...")
                result = run_once(max_rounds)
                writer.writerow(result)

    print(f"Hotovo! Výsledky jsou uložené v {OUTPUT_FILE}")

if __name__ == "__main__":
    main()