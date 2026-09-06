import chess.pgn
from io import StringIO


def parse_pgn(pgn_text: str):
    """
    Parse a single PGN game and return structured game data.
    """

    if not pgn_text or not pgn_text.strip():
        raise ValueError("PGN data cannot be empty.")

    game = chess.pgn.read_game(StringIO(pgn_text))

    if game is None:
        raise ValueError("Invalid PGN data.")

    moves = [move.uci() for move in game.mainline_moves()]

    if not moves:
        raise ValueError("PGN contains no moves.")

    return {
        "headers": dict(game.headers),
        "moves": moves,
        "move_count": len(moves),
    }