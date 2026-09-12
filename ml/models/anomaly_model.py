from sklearn.ensemble import IsolationForest


FEATURE_NAMES = [
    "average_centipawn_loss",
    "median_centipawn_loss",
    "high_centipawn_loss_percentage",
    "top1_agreement_percentage",
    "top3_agreement_percentage",
    "analyzed_move_count",
]


def prepare_features(features: dict) -> list[float]:
    """
    Convert extracted game features into the ordered
    feature vector expected by the ML model.
    """

    missing_features = [
        name for name in FEATURE_NAMES
        if name not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    return [
        float(features[name])
        for name in FEATURE_NAMES
    ]


class AnomalyModel:
    """
    Isolation Forest based anomaly detector.

    The model learns the distribution of normal-looking
    game feature vectors and identifies unusual samples.

    This is an anomaly indicator, not a probability of cheating.
    """

    def __init__(
        self,
        contamination: float = 0.1,
        random_state: int = 42,
    ):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )

    def fit(self, feature_vectors: list[list[float]]):
        """
        Train the anomaly detection model.
        """

        if not feature_vectors:
            raise ValueError(
                "Training data cannot be empty."
            )

        self.model.fit(feature_vectors)
        return self

    def predict(self, feature_vector: list[float]) -> int:
        """
        Predict whether a feature vector is normal or anomalous.

        Returns:
            1  -> normal
            -1 -> anomalous
        """

        return int(
            self.model.predict([feature_vector])[0]
        )

    def anomaly_score(self, feature_vector: list[float]) -> float:
        """
        Return the Isolation Forest anomaly score.

        Lower values indicate more anomalous samples.
        """

        return float(
            self.model.score_samples([feature_vector])[0]
        )