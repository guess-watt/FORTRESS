from backend.app.move_analyzer import (
    calculate_average_centipawn_loss,
    calculate_top1_agreement_percentage,
    calculate_engine_agreement_percentage,
    calculate_analyzed_move_count,
)


def extract_features(results: list[dict]) -> dict:
    """
    Extract behavioral features from move-analysis results.
    """

    if not results:
        raise ValueError("Analysis results cannot be empty.")

    return {
        "average_centipawn_loss": calculate_average_centipawn_loss(
            results
        ),
        "top1_agreement_percentage": calculate_top1_agreement_percentage(
            results
        ),
        "top3_agreement_percentage": calculate_engine_agreement_percentage(
            results
        ),
        "analyzed_move_count": calculate_analyzed_move_count(
            results
        ),
    }