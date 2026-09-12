import chess.pgn


SOURCE_PGN = "data/raw/lichess_db_standard_rated_2013-07.pgn"
OUTPUT_PGN = "data/raw/lichess_sample_5000.pgn"

MAX_SOURCE_GAMES = 50_000
TARGET_GAMES = 5_000
MIN_PLIES = 20


def create_sample():
    selected_games = 0
    inspected_games = 0

    with open(SOURCE_PGN, encoding="utf-8") as source:
        with open(OUTPUT_PGN, "w", encoding="utf-8") as output:

            while (
                inspected_games < MAX_SOURCE_GAMES
                and selected_games < TARGET_GAMES
            ):
                game = chess.pgn.read_game(source)

                if game is None:
                    break

                inspected_games += 1

                headers = game.headers

                # Exclude bot games.
                if (
                    headers.get("WhiteTitle") == "BOT"
                    or headers.get("BlackTitle") == "BOT"
                ):
                    continue

                # Count moves before deciding whether to keep the game.
                move_count = sum(
                    1 for _ in game.mainline_moves()
                )

                # Exclude extremely short games.
                if move_count < MIN_PLIES:
                    continue

                # Write the complete PGN game.
                exporter = chess.pgn.StringExporter(
                    headers=True,
                    variations=False,
                    comments=True,
                )

                output.write(game.accept(exporter))
                output.write("\n\n")

                selected_games += 1

                if selected_games % 500 == 0:
                    print(
                        f"Selected {selected_games}/{TARGET_GAMES} games "
                        f"(inspected {inspected_games})"
                    )

    print()
    print(f"Games inspected: {inspected_games}")
    print(f"Games selected: {selected_games}")
    print(f"Output: {OUTPUT_PGN}")


if __name__ == "__main__":
    create_sample()