#!/usr/bin/env python3
"""Test script to run a single game and verify data looks correct."""

import asyncio
import json
from pathlib import Path

from convergence.runner import run_benchmark, summarize_results


async def main() -> None:
    """Run a test with Claude Haiku using seed words."""
    print("Running 3 test games with Claude Haiku (with seed words)...")
    print("=" * 50)

    # Use Claude Haiku - cheap and fast
    model = "claude-3-haiku-20240307"

    results = await run_benchmark(
        model1=model,
        model2=model,
        num_games=3,
        max_rounds=20,
        output_dir=Path("data/results"),
        verbose=True,
        use_seed_words=True,  # Enable seed words for fair benchmarking
    )

    print("\n" + "=" * 50)
    print("Summary:")
    print(json.dumps(summarize_results(results), indent=2))

    print("\n" + "=" * 50)
    print("Sample result structure:")
    print(json.dumps(results[0], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
