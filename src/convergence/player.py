"""LLM player abstraction using litellm."""

import re
from dataclasses import dataclass

from litellm import acompletion  # pyright: ignore[reportUnknownVariableType]

from convergence.game import GameState

SYSTEM_PROMPT = """\
You are playing a word association game called "Convergence" \
(also known as "Mind Meld").

RULES:
1. Two players each say a word at the same time
2. The goal is for both players to say the SAME word
3. Each round, think of a word that connects BOTH previous words
4. You cannot repeat any word that has been used before

STRATEGY:
- Think of concepts that bridge both words
- Consider common associations, categories, or themes
- Try to converge on simple, common words

Respond with ONLY a single word. No explanations, no punctuation, just the word."""


def extract_word(response: str) -> str | None:
    """Extract a single word from an LLM response.

    Args:
        response: Raw response from the LLM.

    Returns:
        Cleaned word in lowercase, or None if no valid word found.
    """
    if not response or not response.strip():
        return None

    # Remove common punctuation and quotes
    cleaned = re.sub(r'["\'.!?,;:()]', "", response.strip())

    # Take first word if multiple
    words = cleaned.split()
    if not words:
        return None

    return words[0].lower()


@dataclass
class Player:
    """An LLM player in the Convergence game.

    Attributes:
        model: LiteLLM model identifier (e.g., "gemini/gemini-2.5-flash").
        temperature: Sampling temperature for responses.
    """

    model: str
    temperature: float = 1.0

    def build_prompt(self, state: GameState, is_player1: bool) -> str:
        """Build the user prompt for the current game state.

        Args:
            state: Current game state.
            is_player1: Whether this player is player 1.

        Returns:
            User prompt string.
        """
        if state.round == 0:
            # If seed words are set, use them as the starting point
            if state.seed_word1 and state.seed_word2:
                lines = [
                    "Round 1:",
                    f"Your starting word: {state.seed_word1}",
                    f"Opponent's starting word: {state.seed_word2}",
                    "",
                    f"Think of a word that connects '{state.seed_word1}' "
                    f"and '{state.seed_word2}'.",
                    "",
                    f"Words you cannot use: {state.seed_word1}, {state.seed_word2}",
                    "",
                    "Respond with ONLY a single word.",
                ]
                return "\n".join(lines)
            return "Start the game by saying any word. Respond with ONLY a single word."

        # Get the opponent's last word and our last word
        if is_player1:
            my_words = state.player1_words
            opponent_words = state.player2_words
        else:
            my_words = state.player2_words
            opponent_words = state.player1_words

        my_last = my_words[-1] if my_words else None
        opponent_last = opponent_words[-1] if opponent_words else None

        # Build history section
        lines = [f"Round {state.round + 1}:"]

        if my_last and opponent_last:
            lines.append(f"Your last word: {my_last}")
            lines.append(f"Opponent's last word: {opponent_last}")
            lines.append("")
            lines.append(
                f"Think of a word that connects '{my_last}' and '{opponent_last}'."
            )

        # List forbidden words
        used_words = sorted(state.all_words)
        if used_words:
            lines.append("")
            lines.append(f"Words you cannot use (already used): {', '.join(used_words)}")

        lines.append("")
        lines.append("Respond with ONLY a single word. Do not repeat any used words.")

        return "\n".join(lines)

    async def get_word(self, state: GameState, is_player1: bool) -> str | None:
        """Get a word choice from the LLM.

        Args:
            state: Current game state.
            is_player1: Whether this player is player 1.

        Returns:
            The word chosen by the LLM, or None if invalid.
        """
        prompt = self.build_prompt(state, is_player1)

        response = await acompletion(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
            max_tokens=20,  # Just need a single word
        )

        content = response.choices[0].message.content  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue,reportUnknownVariableType]
        return extract_word(content) if content else None  # pyright: ignore[reportUnknownArgumentType]
