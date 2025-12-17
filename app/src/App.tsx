import { GameViewer } from "./components/GameViewer";
import type { GameResult } from "./types";
import "./App.css";

// Sample game data - in production this would be loaded from an API
const sampleGame: GameResult = {
  outcome: "win",
  rounds: 2,
  converged_word: "sand",
  player1_model: "claude-3-haiku-20240307",
  player2_model: "claude-3-haiku-20240307",
  player1_words: ["beach", "sand"],
  player2_words: ["island", "sand"],
  seed_word1: "vacation",
  seed_word2: "rock",
  game_number: 1,
  timestamp: "2025-12-17T08:08:53.877325+00:00",
};

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Convergence Benchmark</h1>
        <p>Evaluating LLM word association and convergence</p>
      </header>

      <main>
        <GameViewer game={sampleGame} />
      </main>

      <footer>
        <a
          href="https://github.com/maxghenis/convergence-benchmark"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
      </footer>
    </div>
  );
}

export default App;
