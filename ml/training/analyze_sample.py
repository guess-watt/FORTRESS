import chess.pgn

from backend.app.move_analyzer import analyze_game
from backend.app.feature_extractor import extract_features


PGN_PATH = "data/raw/lichess_sample_5000.pgn"
TEST_GAMES = 10
STOCKFISH_DEPTH = 15


def analyze_sample():
    analyzed = 0

    with open(PGN_PATH, encoding="utf-8") as pgn_file:

        while analyzed < TEST_GAMES:
            game = chess.pgn.read_game(pgn_file)

            if game is None:
                break

            moves = [
                move.uci()
                for move in game.mainline_moves()
            ]

            print(
                f"\nAnalyzing game {analyzed + 1}/{TEST_GAMES} "
                f"({len(moves)} plies)..."
            )

            results = analyze_game(
                moves,
                depth=STOCKFISH_DEPTH,
            )

            features = extract_features(results)

            print("Features:", features)

            analyzed += 1

    print(f"\nGames analyzed: {analyzed}")


if __name__ == "__main__":
    analyze_sample()