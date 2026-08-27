import os

import chess
import chess.engine


STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")

if not STOCKFISH_PATH:
    raise EnvironmentError(
        "STOCKFISH_PATH environment variable is not set."
    )


board = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

try:
    result = engine.analyse(board, chess.engine.Limit(depth=15))

    print("Best move:", result["pv"][0])
    print("Evaluation:", result["score"])

finally:
    engine.quit()