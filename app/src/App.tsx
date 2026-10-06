import { useState } from "react";
import { GameViewer } from "./components/GameViewer";
import type { GameResult } from "./types";
import benchmarkData from "./benchmarkData.json";
import "./App.css";

const allGames = benchmarkData.results as GameResult[];

function App() {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const game = allGames[selectedIndex];

  // Group games by model pair
  const modelPairs = [
    { label: "Haiku vs Haiku", start: 0 },
    { label: "Sonnet vs Sonnet", start: 12 },
    { label: "Opus vs Opus", start: 24 },
    { label: "Haiku vs Sonnet", start: 36 },
    { label: "Haiku vs Opus", start: 48 },
    { label: "Sonnet vs Opus", start: 60 },
  ];

  const currentPair = modelPairs.find(
    (p, i) => selectedIndex >= p.start && (i === modelPairs.length - 1 || selectedIndex < modelPairs[i + 1].start)
  );

  return (
    <div className="app">
      <header className="app-header">
        <h1>Convergence Benchmark</h1>
        <p>72 games across Claude 4.5 models</p>
      </header>

      <main>
        <div className="game-selector">
          <select
            value={selectedIndex}
            onChange={(e) => setSelectedIndex(Number(e.target.value))}
          >
            {allGames.map((g, i) => (
              <option key={i} value={i}>
                Game {i + 1}: {g.seed_word1} / {g.seed_word2} → {g.outcome === "win" ? g.converged_word : g.outcome} ({g.rounds}r)
              </option>
            ))}
          </select>
          <div className="nav-buttons">
            <button onClick={() => setSelectedIndex(Math.max(0, selectedIndex - 1))} disabled={selectedIndex === 0}>
              ← Prev
            </button>
            <span>{selectedIndex + 1} / {allGames.length}</span>
            <button onClick={() => setSelectedIndex(Math.min(allGames.length - 1, selectedIndex + 1))} disabled={selectedIndex === allGames.length - 1}>
              Next →
            </button>
          </div>
          <div className="model-pair-label">{currentPair?.label}</div>
        </div>

        <GameViewer game={game} />
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
