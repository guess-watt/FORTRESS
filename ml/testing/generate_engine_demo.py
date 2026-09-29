import chess
import chess.engine
import chess.pgn
from datetime import datetime
import random
import os


STOCKFISH_PATH = (
    r"C:\Users\anwin\OneDrive\Desktop\FORTRESS"
    r"\chess_engine\stockfish\stockfish-windows-x86-64-avx2.exe"
)


OUTPUT_DIR = "data/evaluation/raw"


GAME_COUNT = 5
MAX_MOVES = 50


OPENINGS = [
    ["e2e4", "e7e5"],
    ["d2d4", "d7d5"],
    ["c2c4", "e7e5"],
    ["g1f3", "d7d5"],
    ["e2e4", "c7c5"],
]


def generate_game(game_number):

    engine = chess.engine.SimpleEngine.popen_uci(
        STOCKFISH_PATH
    )

    board = chess.Board()

    game = chess.pgn.Game()

    game.headers["Event"] = "FORTRESS Synthetic Engine Assisted"
    game.headers["Site"] = "Local"
    game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
    game.headers["Round"] = str(game_number)
    game.headers["White"] = "Anonymous_Player"
    game.headers["Black"] = "Anonymous_Player"
    game.headers["TimeControl"] = "180+2"
    game.headers["Annotator"] = "FORTRESS"

    node = game

    white_clock = 180
    black_clock = 180


    # Different opening every game
    opening = random.choice(OPENINGS)

    for move in opening:
        move_obj = chess.Move.from_uci(move)

        if move_obj in board.legal_moves:
            node = node.add_variation(move_obj)
            node.comment = (
                f"[%clk 0:{white_clock//60:02d}:{white_clock%60:02d}]"
            )
            board.push(move_obj)


    print(f"\nGenerating game {game_number}/5")


    for move_number in range(MAX_MOVES):

        if board.is_game_over():
            break


        result = engine.play(
            board,
            chess.engine.Limit(depth=15)
        )


        move = result.move


        if board.turn == chess.WHITE:
            white_clock -= 1
            clock = white_clock
        else:
            black_clock -= 1
            clock = black_clock


        node = node.add_variation(move)

        node.comment = (
            f"[%clk 0:{clock//60:02d}:{clock%60:02d}]"
        )


        board.push(move)


        print(
            f"Game {game_number} | "
            f"Move {move_number+1}/{MAX_MOVES}"
        )


    engine.quit()


    if board.turn == chess.BLACK:
        game.headers["Result"] = "1-0"
    else:
        game.headers["Result"] = "0-1"


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    output = (
        f"{OUTPUT_DIR}/engine_demo_{game_number}.pgn"
    )


    with open(output, "w", encoding="utf-8") as f:

        exporter = chess.pgn.StringExporter(
            headers=True,
            variations=False,
            comments=True
        )

        f.write(
            game.accept(exporter)
        )


    print(
        f"Saved: {output}"
    )



if __name__ == "__main__":

    for i in range(1, GAME_COUNT + 1):
        generate_game(i)

    print("\nCompleted 5 engine demo games.")