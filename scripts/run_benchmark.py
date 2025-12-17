#!/usr/bin/env python3
"""Run convergence benchmark between any two models."""

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from convergence.runner import run_benchmark, summarize_results
from convergence.wordlist import generate_factorial_pairs

# Default models (versioned aliases)
DEFAULT_MODELS = {
    # Anthropic Claude 4.5
    "haiku-4.5": "anthropic/claude-haiku-4-5",
    "sonnet-4.5": "anthropic/claude-sonnet-4-5",
    "opus-4.5": "anthropic/claude-opus-4-5",
    # OpenAI GPT-5
    "gpt-5-mini": "openai/gpt-5-mini-2025-08-07",
    "gpt-5.2-instant": "openai/gpt-5.2-instant",
    "gpt-5.2-thinking": "openai/gpt-5.2-thinking",
    "gpt-5.2-pro": "openai/gpt-5.2-pro",
}


def resolve_model(name: str) -> str:
    """Resolve model shorthand to full litellm identifier."""
    return DEFAULT_MODELS.get(name, name)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run convergence benchmark")
    parser.add_argument("model1", help="First model (shorthand or full litellm id)")
    parser.add_argument("model2", help="Second model (shorthand or full litellm id)")
    parser.add_argument("--triplets", type=int, default=4, help="Number of triplets (3 pairs each)")
    parser.add_argument("--max-rounds", type=int, default=50, help="Max rounds per game")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output-dir", type=Path, default=Path("data/results"), help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    model1 = resolve_model(args.model1)
    model2 = resolve_model(args.model2)

    # Generate seed pairs
    seed_pairs = generate_factorial_pairs(
        num_triplets=args.triplets,
        seed=args.seed,
        use_dictionary=True,
        weighted=True,
    )

    print(f"Model 1: {model1}")
    print(f"Model 2: {model2}")
    print(f"Pairs ({len(seed_pairs)}): {seed_pairs}")
    print("=" * 60)

    results = await run_benchmark(
        model1=model1,
        model2=model2,
        num_games=len(seed_pairs),
        max_rounds=args.max_rounds,
        seed_pairs=seed_pairs,
        verbose=args.verbose,
    )

    summary = summarize_results(results)

    print("\n" + "=" * 60)
    print(f"RESULTS: {args.model1} vs {args.model2}")
    print("=" * 60)
    print(f"Win rate: {summary['win_rate']:.1%}")
    if summary['avg_rounds_to_win'] is not None:
        print(f"Avg rounds: {summary['avg_rounds_to_win']:.2f}")
        print(f"Min/Max rounds: {summary['min_rounds_to_win']}-{summary['max_rounds_to_win']}")
    else:
        print("No wins recorded")

    # Save results
    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    m1_short = args.model1.replace("/", "_")
    m2_short = args.model2.replace("/", "_")
    output_path = args.output_dir / f"{m1_short}_vs_{m2_short}_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(
            {
                "metadata": {
                    "model1": model1,
                    "model2": model2,
                    "num_triplets": args.triplets,
                    "max_rounds": args.max_rounds,
                    "seed": args.seed,
                    "timestamp": timestamp,
                },
                "results": results,
                "summary": summary,
            },
            f,
            indent=2,
        )

    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
