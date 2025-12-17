import { GameViewer } from "./components/GameViewer";
import type { GameResult } from "./types";
import gameData from "./gameData.json";
import "./App.css";

const sampleGame = gameData as GameResult;

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
