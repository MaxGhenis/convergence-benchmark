"""Tests for word list and seed word generation."""

import random

from convergence.wordlist import COMMON_NOUNS, get_seed_words


class TestWordList:
    """Tests for the word list."""

    def test_common_nouns_not_empty(self) -> None:
        """Word list should contain words."""
        assert len(COMMON_NOUNS) > 100

    def test_common_nouns_are_lowercase(self) -> None:
        """All words should be lowercase."""
        for word in COMMON_NOUNS:
            assert word == word.lower()

    def test_common_nouns_are_single_words(self) -> None:
        """All entries should be single words (no spaces)."""
        for word in COMMON_NOUNS:
            assert " " not in word


class TestGetSeedWords:
    """Tests for seed word generation."""

    def test_returns_two_different_words(self) -> None:
        """Should return two different words."""
        word1, word2 = get_seed_words()
        assert word1 != word2

    def test_returns_words_from_list(self) -> None:
        """Returned words should be from the word list."""
        word1, word2 = get_seed_words()
        assert word1 in COMMON_NOUNS
        assert word2 in COMMON_NOUNS

    def test_respects_random_seed(self) -> None:
        """Same random seed should give same words."""
        random.seed(42)
        words1 = get_seed_words()
        random.seed(42)
        words2 = get_seed_words()
        assert words1 == words2

    def test_different_seeds_give_different_words(self) -> None:
        """Different seeds should (usually) give different words."""
        random.seed(1)
        words1 = get_seed_words()
        random.seed(2)
        words2 = get_seed_words()
        # With a large word list, collision is very unlikely
        assert words1 != words2
