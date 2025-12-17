"""LLM player abstraction using litellm."""

import re
from dataclasses import dataclass

from litellm import acompletion  # pyright: ignore[reportUnknownVariableType]

from convergence.game import GameState

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
        if is_player1:
            my_words = list(state.player1_words)
            opponent_words = list(state.player2_words)
        else:
            my_words = list(state.player2_words)
            opponent_words = list(state.player1_words)

        # Add seed words as round 0
        if state.seed_word1 and state.seed_word2:
            my_seed = state.seed_word1 if is_player1 else state.seed_word2
            opp_seed = state.seed_word2 if is_player1 else state.seed_word1
            my_words = [my_seed] + my_words
            opponent_words = [opp_seed] + opponent_words

        current_round = len(my_words)

        # Build history
        history_lines = []
        for i, (my_word, opp_word) in enumerate(zip(my_words, opponent_words)):
            history_lines.append(f"Round {i + 1}:")
            history_lines.append(f"You: {my_word}")
            history_lines.append(f"Other: {opp_word}")
            history_lines.append("")

        history = "\n".join(history_lines)

        prompt = f"""You're playing Convergence - the goal is to say the same word as the other player. Don't repeat any word from the history.

{history}
Reply with a single word, nothing else."""

        return prompt

    async def get_word(self, state: GameState, is_player1: bool) -> str | None:
        """Get a word choice from the LLM.

        Args:
            state: Current game state.
            is_player1: Whether this player is player 1.

        Returns:
            The word chosen by the LLM, or None if invalid.
        """
        prompt = self.build_prompt(state, is_player1)

        # Build kwargs - GPT-5 models need reasoning_effort to avoid empty responses
        kwargs: dict[str, object] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": 50,
        }
        if "gpt-5" in self.model:
            kwargs["reasoning_effort"] = "minimal"

        response = await acompletion(**kwargs)  # pyright: ignore[reportArgumentType]

        content = response.choices[0].message.content  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue,reportUnknownVariableType]
        return extract_word(content) if content else None  # pyright: ignore[reportUnknownArgumentType]
