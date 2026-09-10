from ml.models.anomaly_model import (
    FEATURE_NAMES,
    prepare_features,
)


def build_training_dataset(feature_records: list[dict]) -> list[list[float]]:
    """
    Convert extracted feature dictionaries into a training dataset.

    Each feature dictionary represents one analyzed game.
    """

    if not feature_records:
        raise ValueError("Feature records cannot be empty.")

    return [
        prepare_features(features)
        for features in feature_records
    ]


def get_feature_names() -> list[str]:
    """
    Return the ordered feature names used by the ML model.
    """

    return FEATURE_NAMES.copy()