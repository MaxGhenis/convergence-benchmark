#!/usr/bin/env python3
"""Run full benchmark on Claude 4.5 model suite."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from convergence.runner import generate_seed_pairs, run_benchmark, summarize_results

# Claude 4.5 models
MODELS = [
    "anthropic/claude-haiku-4-5",
    "anthropic/claude-sonnet-4-5",
    "anthropic/claude-opus-4-5",
]

# Benchmark parameters
NUM_GAMES = 10  # Per model pair
MAX_ROUNDS = 20
RANDOM_SEED = 42  # For reproducibility


async def main() -> None:
    """Run the full benchmark."""
    output_dir = Path("data/results/claude_4_5_suite")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate fixed seed pairs - SAME pairs used for ALL model combinations
    seed_pairs = generate_seed_pairs(NUM_GAMES, seed=RANDOM_SEED)

    print(f"Generated {len(seed_pairs)} seed pairs with seed={RANDOM_SEED}")
    print("Same pairs used for all 6 model combinations!")
    print(f"Pairs: {seed_pairs}")
    print(f"Models: {MODELS}")
    print("=" * 60)

    all_results = []

    # All model pair combinations (same + cross)
    model_pairs = [
        (MODELS[0], MODELS[0]),  # haiku vs haiku
        (MODELS[1], MODELS[1]),  # sonnet vs sonnet
        (MODELS[2], MODELS[2]),  # opus vs opus
        (MODELS[0], MODELS[1]),  # haiku vs sonnet
        (MODELS[0], MODELS[2]),  # haiku vs opus
        (MODELS[1], MODELS[2]),  # sonnet vs opus
    ]

    for model1, model2 in model_pairs:
        is_same = model1 == model2
        benchmark_type = "same_model" if is_same else "cross_model"
        print(f"\n--- {model1} vs {model2} ---")

        results = await run_benchmark(
            model1=model1,
            model2=model2,
            num_games=NUM_GAMES,
            max_rounds=MAX_ROUNDS,
            seed_pairs=seed_pairs,  # Same pairs for all!
            verbose=True,
        )

        for r in results:
            r["benchmark_type"] = benchmark_type
        all_results.extend(results)

        summary = summarize_results(results)
        print(f"\nSummary: {json.dumps(summary, indent=2)}")

    # Save all results
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"claude_4_5_benchmark_{timestamp}.json"
    with open(output_path, "w") as f:
        json.dump(
            {
                "metadata": {
                    "models": MODELS,
                    "num_games_per_pair": NUM_GAMES,
                    "max_rounds": MAX_ROUNDS,
                    "random_seed": RANDOM_SEED,
                    "timestamp": timestamp,
                },
                "results": all_results,
                "summary": {
                    "total_games": len(all_results),
                    "overall": summarize_results(all_results),
                },
            },
            f,
            indent=2,
        )

    print("\n" + "=" * 60)
    print(f"Results saved to {output_path}")
    print(f"Total games: {len(all_results)}")
    print(f"Overall summary: {json.dumps(summarize_results(all_results), indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
