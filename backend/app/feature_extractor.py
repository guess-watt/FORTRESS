from statistics import median

from backend.app.move_analyzer import (
    calculate_average_centipawn_loss,
    calculate_top1_agreement_percentage,
    calculate_engine_agreement_percentage,
    calculate_analyzed_move_count,
)


def calculate_median_centipawn_loss(results: list[dict]) -> float:
    if not results:
        return 0.0

    centipawn_losses = [
        result["centipawn_loss"]
        for result in results
    ]

    return float(median(centipawn_losses))


def calculate_high_centipawn_loss_percentage(
    results: list[dict],
    threshold: int = 50,
) -> float:
    if not results:
        return 0.0

    high_loss_count = sum(
        1
        for result in results
        if result["centipawn_loss"] >= threshold
    )

    return (high_loss_count / len(results)) * 100


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
        "median_centipawn_loss": calculate_median_centipawn_loss(
            results
        ),
        "high_centipawn_loss_percentage": (
            calculate_high_centipawn_loss_percentage(results)
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