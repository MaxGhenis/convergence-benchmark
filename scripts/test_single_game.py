#!/usr/bin/env python3
"""Test script to run a single game and verify data looks correct."""

import asyncio
import json
from pathlib import Path

from convergence.runner import run_benchmark, summarize_results


async def main() -> None:
    """Run a test with Claude Haiku."""
    print("Running 3 test games with Claude Haiku...")
    print("=" * 50)

    # Use Claude Haiku - cheap and fast
    # litellm format: anthropic/claude-3-haiku-20240307
    model = "claude-3-haiku-20240307"

    results = await run_benchmark(
        model1=model,
        model2=model,
        num_games=3,
        max_rounds=20,
        output_dir=Path("data/results"),
        verbose=True,
    )

    print("\n" + "=" * 50)
    print("Summary:")
    print(json.dumps(summarize_results(results), indent=2))

    print("\n" + "=" * 50)
    print("Sample result structure:")
    print(json.dumps(results[0], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
