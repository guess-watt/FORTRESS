import os

import chess
import chess.engine


STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")


class StockfishAnalyzer:
    """
    Reusable Stockfish analyzer.

    Keeps a single Stockfish engine process open so multiple
    positions can be analyzed efficiently.
    """

    def __init__(self, depth: int = 15):
        if not STOCKFISH_PATH:
            raise EnvironmentError(
                "STOCKFISH_PATH environment variable is not set."
            )

        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(
            STOCKFISH_PATH
        )

    def analyze_position(self, board: chess.Board, top_n: int = 1):
        """
        Analyze a chess position.

        Returns the top engine moves and their evaluations.
        """

        if top_n < 1:
            raise ValueError("top_n must be at least 1.")

        results = self.engine.analyse(
            board,
            chess.engine.Limit(depth=self.depth),
            multipv=top_n,
        )

        # Normalize the result so we always work with a list.
        if not isinstance(results, list):
            results = [results]

        moves = []

        for result in results:
            pv = result.get("pv")

            if not pv:
                continue

            score = result["score"].pov(board.turn)

            evaluation = score.score(mate_score=100000)

            if evaluation is None:
                continue

            moves.append(
                {
                    "move": pv[0].uci(),
                    "evaluation": evaluation,
                }
            )

        if not moves:
            raise ValueError(
                "Stockfish returned no valid principal variation."
            )

        return {
            "moves": moves
        }

    def close(self):
        """Close the Stockfish engine."""
        self.engine.quit()