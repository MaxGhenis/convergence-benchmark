import { useState } from "react";
import type { GameResult, Round } from "../types";

interface GameViewerProps {
  game: GameResult;
}

function getRounds(game: GameResult): Round[] {
  const rounds: Round[] = [];
  for (let i = 0; i < game.player1_words.length; i++) {
    rounds.push({
      number: i + 1,
      player1_word: game.player1_words[i],
      player2_word: game.player2_words[i],
      converged: game.player1_words[i] === game.player2_words[i],
    });
  }
  return rounds;
}

export function GameViewer({ game }: GameViewerProps) {
  const [currentRound, setCurrentRound] = useState(0);
  const rounds = getRounds(game);
  const isPlaying = currentRound > 0;
  const visibleRounds = rounds.slice(0, currentRound);

  const stepForward = () => {
    if (currentRound < rounds.length) {
      setCurrentRound(currentRound + 1);
    }
  };

  const stepBackward = () => {
    if (currentRound > 0) {
      setCurrentRound(currentRound - 1);
    }
  };

  const reset = () => setCurrentRound(0);
  const playAll = () => setCurrentRound(rounds.length);

  return (
    <div className="game-viewer">
      <div className="game-header">
        <h2>Convergence Game</h2>
        <div className="models">
          <span className="model player1">{game.player1_model}</span>
          <span className="vs">vs</span>
          <span className="model player2">{game.player2_model}</span>
        </div>
      </div>

      <div className="seed-words">
        <div className="seed seed1">
          <span className="label">Player 1 Seed</span>
          <span className="word">{game.seed_word1}</span>
        </div>
        <div className="connector">
          <svg viewBox="0 0 100 20" className="arrow">
            <path d="M0,10 L90,10 M80,5 L90,10 L80,15" stroke="currentColor" fill="none" strokeWidth="2"/>
          </svg>
        </div>
        <div className="seed seed2">
          <span className="label">Player 2 Seed</span>
          <span className="word">{game.seed_word2}</span>
        </div>
      </div>

      <div className="timeline">
        {visibleRounds.map((round) => (
          <div
            key={round.number}
            className={`round ${round.converged ? "converged" : ""}`}
          >
            <div className="round-number">Round {round.number}</div>
            <div className="words">
              <div className="word player1">{round.player1_word}</div>
              {round.converged ? (
                <div className="converge-indicator">
                  <span className="checkmark">✓</span>
                </div>
              ) : (
                <div className="diverge-indicator">
                  <span className="x">✗</span>
                </div>
              )}
              <div className="word player2">{round.player2_word}</div>
            </div>
          </div>
        ))}

        {!isPlaying && (
          <div className="start-prompt">
            <p>Click "Step" or "Play All" to see the game unfold</p>
          </div>
        )}

        {currentRound === rounds.length && game.outcome === "win" && (
          <div className="result success">
            <span className="icon">🎉</span>
            <span>Converged on "{game.converged_word}" in {game.rounds} rounds!</span>
          </div>
        )}

        {currentRound === rounds.length && game.outcome !== "win" && (
          <div className="result failure">
            <span className="icon">😞</span>
            <span>Failed to converge ({game.outcome})</span>
          </div>
        )}
      </div>

      <div className="controls">
        <button onClick={reset} disabled={currentRound === 0}>
          Reset
        </button>
        <button onClick={stepBackward} disabled={currentRound === 0}>
          ← Back
        </button>
        <button onClick={stepForward} disabled={currentRound >= rounds.length}>
          Step →
        </button>
        <button onClick={playAll} disabled={currentRound >= rounds.length}>
          Play All
        </button>
      </div>

      <div className="metadata">
        <span>Game #{game.game_number}</span>
        <span>{new Date(game.timestamp).toLocaleString()}</span>
      </div>
    </div>
  );
}
