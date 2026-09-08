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

        # python-chess returns a dictionary for a single PV
        # and a list of dictionaries for multiple PVs.
        if not isinstance(results, list):
            results = [results]

        return {
            "moves": [
                {
                    "move": result["pv"][0].uci(),
                    "evaluation": result["score"].pov(board.turn).score(
                        mate_score=100000
                    ),
                }
                for result in results
            ]
        }

    def close(self):
        """Close the Stockfish engine."""
        self.engine.quit()
