"""Tests for core game logic."""


from convergence.game import Game, GameResult, GameState, Outcome


class TestGameState:
    """Tests for GameState class."""

    def test_initial_state(self) -> None:
        """New game state should have empty history and round 0."""
        state = GameState()
        assert state.round == 0
        assert state.player1_words == ()
        assert state.player2_words == ()
        assert state.is_finished is False

    def test_add_words(self) -> None:
        """Adding words should update state correctly."""
        state = GameState()
        state = state.add_round("apple", "banana")
        assert state.round == 1
        assert state.player1_words == ("apple",)
        assert state.player2_words == ("banana",)

    def test_convergence_detected(self) -> None:
        """State should detect when players say the same word."""
        state = GameState()
        state = state.add_round("apple", "banana")
        assert state.is_finished is False

        state = state.add_round("fruit", "fruit")
        assert state.is_finished is True
        assert state.converged_word == "fruit"

    def test_all_words_property(self) -> None:
        """all_words should return all words used by both players."""
        state = GameState()
        state = state.add_round("apple", "banana")
        state = state.add_round("fruit", "food")
        assert set(state.all_words) == {"apple", "banana", "fruit", "food"}

    def test_seed_words(self) -> None:
        """GameState should store seed words."""
        state = GameState(seed_word1="cat", seed_word2="dog")
        assert state.seed_word1 == "cat"
        assert state.seed_word2 == "dog"

    def test_seed_words_in_all_words(self) -> None:
        """Seed words should be included in all_words."""
        state = GameState(seed_word1="cat", seed_word2="dog")
        assert "cat" in state.all_words
        assert "dog" in state.all_words

    def test_seed_words_cannot_be_used(self) -> None:
        """Seed words should count as already used."""
        state = GameState(seed_word1="cat", seed_word2="dog")
        state = state.add_round("pet", "animal")
        # cat and dog are still in all_words
        assert "cat" in state.all_words
        assert "dog" in state.all_words
        assert "pet" in state.all_words


class TestGameResult:
    """Tests for GameResult class."""

    def test_win_result(self) -> None:
        """Win result should have correct properties."""
        state = GameState()
        state = state.add_round("apple", "banana")
        state = state.add_round("fruit", "fruit")

        result = GameResult(
            outcome=Outcome.WIN,
            rounds=2,
            converged_word="fruit",
            state=state,
            player1_model="gemini-2.5-flash",
            player2_model="gemini-2.5-flash",
        )
        assert result.outcome == Outcome.WIN
        assert result.rounds == 2
        assert result.converged_word == "fruit"

    def test_loss_non_convergence(self) -> None:
        """Non-convergence should be recorded."""
        state = GameState()
        for i in range(20):
            state = state.add_round(f"word{i}a", f"word{i}b")

        result = GameResult(
            outcome=Outcome.NON_CONVERGENCE,
            rounds=20,
            converged_word=None,
            state=state,
            player1_model="gemini-2.5-flash",
            player2_model="gemini-2.5-flash",
        )
        assert result.outcome == Outcome.NON_CONVERGENCE
        assert result.converged_word is None

    def test_to_dict(self) -> None:
        """Result should serialize to dict for JSON export."""
        state = GameState()
        state = state.add_round("fruit", "fruit")

        result = GameResult(
            outcome=Outcome.WIN,
            rounds=1,
            converged_word="fruit",
            state=state,
            player1_model="model1",
            player2_model="model2",
        )
        d = result.to_dict()
        assert d["outcome"] == "win"
        assert d["rounds"] == 1
        assert d["converged_word"] == "fruit"
        assert d["player1_model"] == "model1"
        assert d["player2_model"] == "model2"
        assert "player1_words" in d
        assert "player2_words" in d

    def test_to_dict_with_seed_words(self) -> None:
        """Result should include seed words in serialization."""
        state = GameState(seed_word1="cat", seed_word2="dog")
        state = state.add_round("pet", "pet")

        result = GameResult(
            outcome=Outcome.WIN,
            rounds=1,
            converged_word="pet",
            state=state,
            player1_model="model1",
            player2_model="model2",
        )
        d = result.to_dict()
        assert d["seed_word1"] == "cat"
        assert d["seed_word2"] == "dog"


class TestGame:
    """Tests for Game orchestration."""

    def test_max_rounds_limit(self) -> None:
        """Game should stop after max rounds."""
        game = Game(max_rounds=5)
        assert game.max_rounds == 5

    def test_word_repetition_not_allowed(self) -> None:
        """Words used before should not be allowed."""
        state = GameState()
        state = state.add_round("apple", "banana")

        # apple is already used
        assert "apple" in state.all_words
        assert "banana" in state.all_words
        assert "fruit" not in state.all_words
