import unittest

from ml.training.dataset import (
    build_training_dataset,
    get_feature_names,
)


class TestDataset(unittest.TestCase):

    def setUp(self):
        self.feature_records = [
            {
                "average_centipawn_loss": 15.0,
                "top1_agreement_percentage": 70.0,
                "top3_agreement_percentage": 90.0,
                "analyzed_move_count": 40,
            },
            {
                "average_centipawn_loss": 20.0,
                "top1_agreement_percentage": 65.0,
                "top3_agreement_percentage": 85.0,
                "analyzed_move_count": 35,
            },
        ]

    def test_build_training_dataset(self):
        dataset = build_training_dataset(
            self.feature_records
        )

        self.assertEqual(
            dataset,
            [
                [15.0, 70.0, 90.0, 40.0],
                [20.0, 65.0, 85.0, 35.0],
            ],
        )

    def test_dataset_contains_one_vector_per_game(self):
        dataset = build_training_dataset(
            self.feature_records
        )

        self.assertEqual(len(dataset), 2)

    def test_feature_order(self):
        feature_names = get_feature_names()

        self.assertEqual(
            feature_names,
            [
                "average_centipawn_loss",
                "top1_agreement_percentage",
                "top3_agreement_percentage",
                "analyzed_move_count",
            ],
        )

    def test_empty_records(self):
        with self.assertRaises(ValueError):
            build_training_dataset([])


if __name__ == "__main__":
    unittest.main()