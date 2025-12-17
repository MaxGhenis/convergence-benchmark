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

    # Generate fixed seed pairs for all games
    # Same-model: 3 models × 10 games = 30 pairs
    # Cross-model: 3 pairs × 10 games = 30 pairs
    # Total: 60 pairs
    total_games = len(MODELS) * NUM_GAMES + 3 * NUM_GAMES  # same + cross
    seed_pairs = generate_seed_pairs(total_games, seed=RANDOM_SEED)

    print(f"Generated {len(seed_pairs)} seed pairs with seed={RANDOM_SEED}")
    print(f"Models: {MODELS}")
    print(f"Games per pair: {NUM_GAMES}")
    print("=" * 60)

    all_results = []
    pair_idx = 0

    # Same-model games
    print("\n=== SAME-MODEL GAMES ===")
    for model in MODELS:
        print(f"\n--- {model} vs {model} ---")
        pairs = seed_pairs[pair_idx : pair_idx + NUM_GAMES]
        pair_idx += NUM_GAMES

        results = await run_benchmark(
            model1=model,
            model2=model,
            num_games=NUM_GAMES,
            max_rounds=MAX_ROUNDS,
            seed_pairs=pairs,
            verbose=True,
        )

        for r in results:
            r["benchmark_type"] = "same_model"
        all_results.extend(results)

        summary = summarize_results(results)
        print(f"\nSummary: {json.dumps(summary, indent=2)}")

    # Cross-model games
    print("\n=== CROSS-MODEL GAMES ===")
    cross_pairs = [
        (MODELS[0], MODELS[1]),  # haiku vs sonnet
        (MODELS[0], MODELS[2]),  # haiku vs opus
        (MODELS[1], MODELS[2]),  # sonnet vs opus
    ]

    for model1, model2 in cross_pairs:
        print(f"\n--- {model1} vs {model2} ---")
        pairs = seed_pairs[pair_idx : pair_idx + NUM_GAMES]
        pair_idx += NUM_GAMES

        results = await run_benchmark(
            model1=model1,
            model2=model2,
            num_games=NUM_GAMES,
            max_rounds=MAX_ROUNDS,
            seed_pairs=pairs,
            verbose=True,
        )

        for r in results:
            r["benchmark_type"] = "cross_model"
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
