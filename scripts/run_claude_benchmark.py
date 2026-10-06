#!/usr/bin/env python3
"""Run full benchmark on Claude 4.5 model suite."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from convergence.runner import run_benchmark, summarize_results
from convergence.wordlist import generate_factorial_pairs

# Claude 4.5 models
MODELS = [
    "anthropic/claude-haiku-4-5",
    "anthropic/claude-sonnet-4-5",
    "anthropic/claude-opus-4-5",
]

# Benchmark parameters
NUM_TRIPLETS = 4  # 4 triplets = 12 pairs (factorial design)
MAX_ROUNDS = 50  # Increased to ensure convergence (retries on repeated words)
RANDOM_SEED = 42  # For reproducibility


async def main() -> None:
    """Run the full benchmark."""
    output_dir = Path("data/results/claude_4_5_suite")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate factorial pairs - weighted by word frequency from diverse word list
    # Each triplet (A, B, C) produces 3 pairs: (A,B), (A,C), (B,C)
    # This enables analysis of word-specific effects
    seed_pairs = generate_factorial_pairs(
        num_triplets=NUM_TRIPLETS,
        seed=RANDOM_SEED,
        use_dictionary=True,  # Use diverse ~1000 word list
        weighted=True,  # Weight by word frequency
    )

    print(f"Generated {len(seed_pairs)} seed pairs using factorial design")
    print(f"  - {NUM_TRIPLETS} triplets × 3 pairs each = {len(seed_pairs)} pairs")
    print("  - Words weighted by frequency (common words more likely)")
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

        num_games = len(seed_pairs)
        results = await run_benchmark(
            model1=model1,
            model2=model2,
            num_games=num_games,
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
                    "num_triplets": NUM_TRIPLETS,
                    "num_pairs_per_model_combo": len(seed_pairs),
                    "max_rounds": MAX_ROUNDS,
                    "random_seed": RANDOM_SEED,
                    "timestamp": timestamp,
                    "design": "factorial",
                    "word_source": "diverse_words",
                    "weighted_sampling": True,
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
