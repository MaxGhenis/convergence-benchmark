"""Core game logic for the Convergence word association game."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Outcome(Enum):
    """Possible outcomes of a Convergence game."""

    WIN = "win"
    NON_CONVERGENCE = "non_convergence"
    REPETITION = "repetition"
    INVALID_WORD = "invalid_word"


@dataclass(frozen=True)
class GameState:
    """Immutable state of a Convergence game.

    Attributes:
        round: Current round number (0-indexed before first move).
        player1_words: Words chosen by player 1.
        player2_words: Words chosen by player 2.
    """

    round: int = 0
    player1_words: tuple[str, ...] = field(default_factory=tuple)
    player2_words: tuple[str, ...] = field(default_factory=tuple)

    def add_round(self, word1: str, word2: str) -> "GameState":
        """Add a round with words from both players.

        Args:
            word1: Word chosen by player 1.
            word2: Word chosen by player 2.

        Returns:
            New GameState with the round added.
        """
        return GameState(
            round=self.round + 1,
            player1_words=(*self.player1_words, word1.lower().strip()),
            player2_words=(*self.player2_words, word2.lower().strip()),
        )

    @property
    def is_finished(self) -> bool:
        """Check if the game has finished (players said the same word)."""
        if not self.player1_words or not self.player2_words:
            return False
        return self.player1_words[-1] == self.player2_words[-1]

    @property
    def converged_word(self) -> str | None:
        """Get the word both players converged on, if any."""
        if self.is_finished and self.player1_words:
            return self.player1_words[-1]
        return None

    @property
    def all_words(self) -> set[str]:
        """Get all words used by both players."""
        return set(self.player1_words) | set(self.player2_words)


@dataclass
class GameResult:
    """Result of a completed Convergence game.

    Attributes:
        outcome: How the game ended.
        rounds: Number of rounds played.
        converged_word: The word both players said (if WIN).
        state: Final game state.
        player1_model: Model identifier for player 1.
        player2_model: Model identifier for player 2.
    """

    outcome: Outcome
    rounds: int
    converged_word: str | None
    state: GameState
    player1_model: str
    player2_model: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize result to dictionary for JSON export."""
        return {
            "outcome": self.outcome.value,
            "rounds": self.rounds,
            "converged_word": self.converged_word,
            "player1_model": self.player1_model,
            "player2_model": self.player2_model,
            "player1_words": list(self.state.player1_words),
            "player2_words": list(self.state.player2_words),
        }


@dataclass
class Game:
    """Orchestrates a Convergence game between two players.

    Attributes:
        max_rounds: Maximum rounds before declaring non-convergence.
    """

    max_rounds: int = 20
