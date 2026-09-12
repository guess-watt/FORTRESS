import chess.pgn
from collections import Counter


PGN_PATH = "data/raw/lichess_db_standard_rated_2013-07.pgn"
MAX_GAMES = 50_000


def inspect_dataset():
    time_controls = Counter()
    termination = Counter()

    bot_games = 0
    clock_games = 0
    game_lengths = Counter()

    total_games = 0

    with open(PGN_PATH, encoding="utf-8") as pgn_file:
        for total_games in range(1, MAX_GAMES + 1):
            game = chess.pgn.read_game(pgn_file)

            if game is None:
                break

            headers = game.headers

            time_controls[headers.get("TimeControl", "?")] += 1
            termination[headers.get("Termination", "?")] += 1

            if (
                headers.get("WhiteTitle") == "BOT"
                or headers.get("BlackTitle") == "BOT"
            ):
                bot_games += 1

            move_count = 0
            has_clock = False

            for node in game.mainline():
                move_count += 1

                if "%clk" in node.comment:
                    has_clock = True

            if has_clock:
                clock_games += 1

            if move_count < 20:
                game_lengths["<20 plies"] += 1
            elif move_count < 60:
                game_lengths["20-59 plies"] += 1
            else:
                game_lengths["60+ plies"] += 1

            if total_games % 10_000 == 0:
                print(f"Games inspected: {total_games}")

    print(f"\nGames inspected: {total_games}")
    print(f"Bot games: {bot_games}")
    print(f"Games with clock data: {clock_games}")

    print("\nTime controls:")
    for value, count in time_controls.most_common():
        print(f"  {value}: {count}")

    print("\nGame lengths:")
    for value, count in game_lengths.items():
        print(f"  {value}: {count}")

    print("\nTermination:")
    for value, count in termination.most_common():
        print(f"  {value}: {count}")


if __name__ == "__main__":
    inspect_dataset()