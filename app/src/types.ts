export interface GameResult {
  outcome: "win" | "non_convergence" | "repetition" | "invalid_word";
  rounds: number;
  converged_word: string | null;
  player1_model: string;
  player2_model: string;
  player1_words: string[];
  player2_words: string[];
  seed_word1: string;
  seed_word2: string;
  game_number: number;
  timestamp: string;
}

export interface Round {
  number: number;
  player1_word: string;
  player2_word: string;
  converged: boolean;
}
