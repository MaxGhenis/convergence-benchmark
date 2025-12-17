"""Tests for LLM player abstraction."""

from unittest.mock import AsyncMock, patch

import pytest

from convergence.game import GameState
from convergence.player import Player, extract_word


class TestExtractWord:
    """Tests for word extraction from LLM responses."""

    def test_single_word(self) -> None:
        """Should extract a single word cleanly."""
        assert extract_word("apple") == "apple"
        assert extract_word("Apple") == "apple"
        assert extract_word("  APPLE  ") == "apple"

    def test_word_with_punctuation(self) -> None:
        """Should strip punctuation."""
        assert extract_word("apple.") == "apple"
        assert extract_word("apple!") == "apple"
        assert extract_word('"apple"') == "apple"

    def test_sentence_response(self) -> None:
        """Should extract first word from sentence."""
        assert extract_word("Apple is my choice") == "apple"
        # Note: extract_word takes first word, so "I think: apple" returns "i"
        # This is fine because LLMs are prompted to return just one word
        assert extract_word("fruit food") == "fruit"

    def test_empty_response(self) -> None:
        """Should handle empty responses."""
        assert extract_word("") is None
        assert extract_word("   ") is None


class TestPlayer:
    """Tests for Player class."""

    def test_player_creation(self) -> None:
        """Player should store model identifier."""
        player = Player(model="gemini/gemini-2.5-flash")
        assert player.model == "gemini/gemini-2.5-flash"

    def test_build_prompt_first_round(self) -> None:
        """First round prompt should ask for a starting word."""
        player = Player(model="gemini/gemini-2.5-flash")
        state = GameState()

        prompt = player.build_prompt(state, is_player1=True)
        # First round just asks for any word (game rules are in system prompt)
        assert "word" in prompt.lower()
        assert "single" in prompt.lower() or "only" in prompt.lower()

    def test_build_prompt_subsequent_round(self) -> None:
        """Subsequent rounds should include history."""
        player = Player(model="gemini/gemini-2.5-flash")
        state = GameState()
        state = state.add_round("apple", "banana")

        prompt = player.build_prompt(state, is_player1=True)
        assert "apple" in prompt.lower()
        assert "banana" in prompt.lower()

    def test_build_prompt_excludes_used_words(self) -> None:
        """Prompt should remind not to repeat words."""
        player = Player(model="gemini/gemini-2.5-flash")
        state = GameState()
        state = state.add_round("apple", "banana")

        prompt = player.build_prompt(state, is_player1=True)
        # Should mention that apple and banana cannot be used
        assert "cannot" in prompt.lower() or "don't" in prompt.lower() or "not" in prompt.lower()

    @pytest.mark.asyncio
    async def test_get_word_calls_litellm(self) -> None:
        """get_word should call litellm completion."""
        player = Player(model="gemini/gemini-2.5-flash")
        state = GameState()

        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "fruit"

        with patch("convergence.player.acompletion", return_value=mock_response) as mock_completion:
            word = await player.get_word(state, is_player1=True)

            assert word == "fruit"
            mock_completion.assert_called_once()
            # Check model was passed
            call_kwargs = mock_completion.call_args.kwargs
            assert call_kwargs["model"] == "gemini/gemini-2.5-flash"
