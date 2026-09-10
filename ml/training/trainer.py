from ml.models.anomaly_model import AnomalyModel
from ml.training.dataset import build_training_dataset


def train_anomaly_model(
    feature_records: list[dict],
    contamination: float = 0.1,
    random_state: int = 42,
) -> AnomalyModel:
    """
    Build a training dataset and train an Isolation Forest model.
    """

    training_dataset = build_training_dataset(feature_records)

    model = AnomalyModel(
        contamination=contamination,
        random_state=random_state,
    )

    model.fit(training_dataset)

    return model