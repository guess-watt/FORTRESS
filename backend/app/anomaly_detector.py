def calculate_anomaly_score(features: dict) -> float:
    """
    Calculate a rule-based anomaly score from extracted features.

    The score ranges from 0 to 100.
    A higher score indicates more statistically unusual
    engine-like behavior.

    This score does not prove cheating.
    """

    required_features = {
        "average_centipawn_loss",
        "top1_agreement_percentage",
        "top3_agreement_percentage",
        "analyzed_move_count",
    }

    missing_features = required_features - features.keys()

    if missing_features:
        raise ValueError(
            f"Missing required features: {sorted(missing_features)}"
        )

    if features["analyzed_move_count"] <= 0:
        raise ValueError("analyzed_move_count must be greater than 0.")

    score = 0.0

    # Very low average centipawn loss.
    if features["average_centipawn_loss"] <= 10:
        score += 30
    elif features["average_centipawn_loss"] <= 20:
        score += 20
    elif features["average_centipawn_loss"] <= 30:
        score += 10

    # High top-1 engine agreement.
    if features["top1_agreement_percentage"] >= 80:
        score += 35
    elif features["top1_agreement_percentage"] >= 65:
        score += 25
    elif features["top1_agreement_percentage"] >= 50:
        score += 15

    # High top-3 engine agreement.
    if features["top3_agreement_percentage"] >= 95:
        score += 25
    elif features["top3_agreement_percentage"] >= 85:
        score += 15
    elif features["top3_agreement_percentage"] >= 75:
        score += 10

    return min(score, 100.0)


def get_anomaly_reasons(features: dict) -> list[str]:
    """
    Return human-readable reasons for elevated anomaly indicators.
    """

    reasons = []

    if features["average_centipawn_loss"] <= 10:
        reasons.append(
            "Very low average centipawn loss."
        )
    elif features["average_centipawn_loss"] <= 20:
        reasons.append(
            "Low average centipawn loss."
        )

    if features["top1_agreement_percentage"] >= 80:
        reasons.append(
            "Very high top-1 engine agreement."
        )
    elif features["top1_agreement_percentage"] >= 65:
        reasons.append(
            "High top-1 engine agreement."
        )

    if features["top3_agreement_percentage"] >= 95:
        reasons.append(
            "Very high top-3 engine agreement."
        )
    elif features["top3_agreement_percentage"] >= 85:
        reasons.append(
            "High top-3 engine agreement."
        )

    return reasons