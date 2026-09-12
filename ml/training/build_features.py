import csv

import chess.pgn

from backend.app.move_analyzer import analyze_game
from backend.app.feature_extractor import extract_features


SOURCE_PGN = "data/raw/lichess_sample_5000.pgn"
OUTPUT_CSV = "data/processed/features.csv"

MAX_GAMES = 25
STOCKFISH_DEPTH = 15


def build_features():
    processed_games = 0

    fieldnames = [
        "average_centipawn_loss",
        "top1_agreement_percentage",
        "top3_agreement_percentage",
        "analyzed_move_count",
    ]

    with open(SOURCE_PGN, encoding="utf-8") as pgn_file:
        with open(
            OUTPUT_CSV,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            while processed_games < MAX_GAMES:
                game = chess.pgn.read_game(pgn_file)

                if game is None:
                    break

                moves = [
                    move.uci()
                    for move in game.mainline_moves()
                ]

                if not moves:
                    continue

                print(
                    f"Analyzing game "
                    f"{processed_games + 1}/{MAX_GAMES} "
                    f"({len(moves)} plies)..."
                )

                results = analyze_game(
                    moves,
                    depth=STOCKFISH_DEPTH,
                )

                features = extract_features(results)

                writer.writerow(features)

                processed_games += 1

    print()
    print(f"Games processed: {processed_games}")
    print(f"Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    build_features()