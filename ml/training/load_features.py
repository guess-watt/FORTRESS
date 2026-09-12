import csv


FEATURES_CSV = "data/processed/features.csv"


def load_feature_records(csv_path: str = FEATURES_CSV) -> list[dict]:
    """
    Load extracted game features from a CSV file.

    Each row represents one analyzed game.
    """

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        records = []

        for row in reader:
            records.append(
                {
                    key: float(value)
                    for key, value in row.items()
                }
            )

    if not records:
        raise ValueError("Feature CSV contains no records.")

    return records