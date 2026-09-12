from ml.models.anomaly_model import prepare_features
from ml.training.load_features import load_feature_records
from ml.training.trainer import train_anomaly_model


def main():
    feature_records = load_feature_records()

    model = train_anomaly_model(
        feature_records,
        contamination=0.1,
        random_state=42,
    )

    print(f"Training records: {len(feature_records)}")
    print("\nPredictions:")

    for index, features in enumerate(
        feature_records,
        start=1,
    ):
        feature_vector = prepare_features(features)

        prediction = model.predict(feature_vector)
        score = model.anomaly_score(feature_vector)

        label = (
            "ANOMALOUS"
            if prediction == -1
            else "NORMAL"
        )

        print(
            f"Game {index:02d}: "
            f"{label} | "
            f"Isolation score: {score:.4f}"
        )


if __name__ == "__main__":
    main()