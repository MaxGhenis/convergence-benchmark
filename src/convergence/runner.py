"""Game runner for executing Convergence games between LLMs."""

import asyncio
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from convergence.game import GameResult, GameState, Outcome
from convergence.player import Player
from convergence.wordlist import get_seed_words


@dataclass
class GameRunner:
    """Runs Convergence games between two LLM players.

    Attributes:
        player1: First player.
        player2: Second player.
        max_rounds: Maximum rounds before declaring non-convergence.
        verbose: Whether to print progress.
    """

    player1: Player
    player2: Player
    max_rounds: int = 20
    verbose: bool = False

    async def play_game(
        self, seed_word1: str | None = None, seed_word2: str | None = None
    ) -> GameResult:
        """Play a single game between the two players.

        Args:
            seed_word1: Optional starting word for player 1.
            seed_word2: Optional starting word for player 2.

        Returns:
            GameResult with the outcome and full history.
        """
        state = GameState(seed_word1=seed_word1, seed_word2=seed_word2)

        for round_num in range(self.max_rounds):
            # Get words from both players concurrently
            word1_task = self.player1.get_word(state, is_player1=True)
            word2_task = self.player2.get_word(state, is_player1=False)

            word1, word2 = await asyncio.gather(word1_task, word2_task)

            if self.verbose:
                print(f"Round {round_num + 1}: '{word1}' vs '{word2}'")

            # Check for invalid words
            if word1 is None or word2 is None:
                return GameResult(
                    outcome=Outcome.INVALID_WORD,
                    rounds=round_num + 1,
                    converged_word=None,
                    state=state,
                    player1_model=self.player1.model,
                    player2_model=self.player2.model,
                )

            # Check for repetition
            if word1 in state.all_words or word2 in state.all_words:
                # Record the attempt anyway
                state = state.add_round(word1, word2)
                return GameResult(
                    outcome=Outcome.REPETITION,
                    rounds=round_num + 1,
                    converged_word=None,
                    state=state,
                    player1_model=self.player1.model,
                    player2_model=self.player2.model,
                )

            # Add the round
            state = state.add_round(word1, word2)

            # Check for convergence
            if state.is_finished:
                if self.verbose:
                    print(f"Converged on '{state.converged_word}'!")
                return GameResult(
                    outcome=Outcome.WIN,
                    rounds=round_num + 1,
                    converged_word=state.converged_word,
                    state=state,
                    player1_model=self.player1.model,
                    player2_model=self.player2.model,
                )

        # Reached max rounds without convergence
        return GameResult(
            outcome=Outcome.NON_CONVERGENCE,
            rounds=self.max_rounds,
            converged_word=None,
            state=state,
            player1_model=self.player1.model,
            player2_model=self.player2.model,
        )


async def run_benchmark(
    model1: str,
    model2: str,
    num_games: int = 10,
    max_rounds: int = 20,
    output_dir: Path | None = None,
    verbose: bool = False,
    use_seed_words: bool = True,
) -> list[dict[str, Any]]:
    """Run a benchmark of multiple games between two models.

    Args:
        model1: LiteLLM model identifier for player 1.
        model2: LiteLLM model identifier for player 2.
        num_games: Number of games to play.
        max_rounds: Maximum rounds per game.
        output_dir: Directory to save results (optional).
        verbose: Whether to print progress.
        use_seed_words: Whether to assign random seed words (default True).

    Returns:
        List of game results as dictionaries.
    """
    player1 = Player(model=model1)
    player2 = Player(model=model2)
    runner = GameRunner(player1, player2, max_rounds=max_rounds, verbose=verbose)

    results: list[dict[str, Any]] = []

    for i in range(num_games):
        # Generate seed words for fair benchmarking
        if use_seed_words:
            seed_word1, seed_word2 = get_seed_words()
        else:
            seed_word1, seed_word2 = None, None

        if verbose:
            print(f"\n=== Game {i + 1}/{num_games} ===")
            if seed_word1 and seed_word2:
                print(f"Seed words: '{seed_word1}' vs '{seed_word2}'")

        result = await runner.play_game(seed_word1, seed_word2)
        result_dict = result.to_dict()
        result_dict["game_number"] = i + 1
        result_dict["timestamp"] = datetime.now(UTC).isoformat()
        results.append(result_dict)

        if verbose:
            print(f"Outcome: {result.outcome.value}, Rounds: {result.rounds}")

    # Save results if output directory specified
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"{model1.replace('/', '_')}_vs_{model2.replace('/', '_')}_{timestamp}.json"
        output_path = output_dir / filename
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        if verbose:
            print(f"\nResults saved to {output_path}")

    return results


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute summary statistics from game results.

    Args:
        results: List of game result dictionaries.

    Returns:
        Dictionary with summary statistics.
    """
    total = len(results)
    wins = sum(1 for r in results if r["outcome"] == "win")
    rounds_to_win = [r["rounds"] for r in results if r["outcome"] == "win"]

    return {
        "total_games": total,
        "wins": wins,
        "win_rate": wins / total if total > 0 else 0,
        "non_convergence": sum(1 for r in results if r["outcome"] == "non_convergence"),
        "repetitions": sum(1 for r in results if r["outcome"] == "repetition"),
        "invalid_words": sum(1 for r in results if r["outcome"] == "invalid_word"),
        "avg_rounds_to_win": sum(rounds_to_win) / len(rounds_to_win) if rounds_to_win else None,
        "min_rounds_to_win": min(rounds_to_win) if rounds_to_win else None,
        "max_rounds_to_win": max(rounds_to_win) if rounds_to_win else None,
    }
