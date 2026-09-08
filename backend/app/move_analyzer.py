import chess

from backend.app.stockfish import StockfishAnalyzer


def analyze_game(moves: list[str], depth: int = 15):
    """
    Analyze every move in a chess game.
    """

    if not moves:
        raise ValueError("Moves cannot be empty.")

    board = chess.Board()
    analyzer = StockfishAnalyzer(depth=depth)

    results = []

    try:
        for ply, move_uci in enumerate(moves, start=1):
            move = chess.Move.from_uci(move_uci)

            if move not in board.legal_moves:
                raise ValueError(
                    f"Illegal move at ply {ply}: {move_uci}"
                )

            player = board.turn
            move_number = board.fullmove_number

            # Engine evaluation before the move.
            analysis_before = analyzer.analyze_position(
                board,
                top_n=3,
            )

            top_engine_moves = [
                item["move"]
                for item in analysis_before["moves"]
            ]

            best_move = top_engine_moves[0]

            evaluation_before = analysis_before["moves"][0]["evaluation"]

            # Play the candidate move.
            board.push(move)

            # Engine evaluation after the move.
            analysis_after = analyzer.analyze_position(
                board,
                top_n=1,
            )

            evaluation_after = analysis_after["moves"][0]["evaluation"]
            # Stockfish reports evaluation from the side-to-move
            # perspective. After the move, that is the opponent.
            # Convert it back to the perspective of the player
            # who made the move.
            evaluation_after_for_player = -evaluation_after

            # Centipawn loss from the player's perspective.
            centipawn_loss = max(
                0,
                evaluation_before - evaluation_after_for_player,
            )

            results.append(
                {
                    "ply": ply,
                    "move_number": move_number,
                    "player": (
                        "White"
                        if player == chess.WHITE
                        else "Black"
                    ),
                    "played_move": move_uci,
                    "best_move": best_move,
                    "top_engine_moves": top_engine_moves,
                    "engine_rank": (
                        top_engine_moves.index(move_uci) + 1
                        if move_uci in top_engine_moves
                        else None
                    ),
                    "engine_agreement": (
                        True
                        if move_uci in top_engine_moves
                        else False
                    ),
                    "evaluation_before": evaluation_before,
                    "evaluation_after": evaluation_after_for_player,
                    "centipawn_loss": centipawn_loss,
                }
            )

    finally:
        analyzer.close()

    return results

def calculate_engine_agreement_percentage(results: list[dict]) -> float:
    """
    Calculate the percentage of moves that were among
    Stockfish's top engine choices.
    """

    if not results:
        return 0.0

    agreement_count = sum(
        1
        for result in results
        if result["engine_agreement"]
    )

    return (agreement_count / len(results)) * 100

def calculate_average_centipawn_loss(results: list[dict]) -> float:
    """
    Calculate the average centipawn loss across all analyzed moves.
    """

    if not results:
        return 0.0

    total_centipawn_loss = sum(
        result["centipawn_loss"]
        for result in results
    )

    return total_centipawn_loss / len(results)


def calculate_top1_agreement_percentage(results: list[dict]) -> float:
    """
    Calculate the percentage of moves that matched
    Stockfish's top-ranked move.
    """

    if not results:
        return 0.0

    top1_count = sum(
        1
        for result in results
        if result["engine_rank"] == 1
    )

    return (top1_count / len(results)) * 100

def calculate_analyzed_move_count(results: list[dict]) -> int:
    """
    Return the number of successfully analyzed moves.
    """

    return len(results)

def calculate_game_summary(results: list[dict]) -> dict:
    """
    Calculate summary statistics for an analyzed game.
    """

    return {
        "move_count": calculate_analyzed_move_count(results),
        "average_centipawn_loss": calculate_average_centipawn_loss(results),
        "top1_agreement_percentage": calculate_top1_agreement_percentage(results),
        "top3_agreement_percentage": calculate_engine_agreement_percentage(results),
    }