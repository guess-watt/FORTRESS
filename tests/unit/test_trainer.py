import unittest

from ml.models.anomaly_model import AnomalyModel
from ml.training.trainer import train_anomaly_model


class TestTrainer(unittest.TestCase):

    def setUp(self):
        self.feature_records = [
            {
                "average_centipawn_loss": 15.0,
                "median_centipawn_loss": 12.0,
                "high_centipawn_loss_percentage": 10.0,
                "top1_agreement_percentage": 70.0,
                "top3_agreement_percentage": 90.0,
                "analyzed_move_count": 40,
            },
            {
                "average_centipawn_loss": 20.0,
                "median_centipawn_loss": 18.0,
                "high_centipawn_loss_percentage": 20.0,
                "top1_agreement_percentage": 65.0,
                "top3_agreement_percentage": 85.0,
                "analyzed_move_count": 35,
            },
            {
                "average_centipawn_loss": 25.0,
                "median_centipawn_loss": 22.0,
                "high_centipawn_loss_percentage": 30.0,
                "top1_agreement_percentage": 60.0,
                "top3_agreement_percentage": 80.0,
                "analyzed_move_count": 45,
            },
            {
                "average_centipawn_loss": 18.0,
                "median_centipawn_loss": 15.0,
                "high_centipawn_loss_percentage": 12.0,
                "top1_agreement_percentage": 72.0,
                "top3_agreement_percentage": 88.0,
                "analyzed_move_count": 50,
            },
            {
                "average_centipawn_loss": 22.0,
                "median_centipawn_loss": 19.0,
                "high_centipawn_loss_percentage": 25.0,
                "top1_agreement_percentage": 68.0,
                "top3_agreement_percentage": 82.0,
                "analyzed_move_count": 42,
            },
        ]

    def test_train_anomaly_model(self):
        model = train_anomaly_model(
            self.feature_records
        )

        self.assertIsInstance(
            model,
            AnomalyModel,
        )

    def test_trained_model_can_predict(self):
        model = train_anomaly_model(
            self.feature_records
        )

        prediction = model.predict(
            [19.0, 16.0, 15.0, 69.0, 87.0, 41.0]
        )

        self.assertIn(prediction, [1, -1])

    def test_custom_contamination(self):
        model = train_anomaly_model(
            self.feature_records,
            contamination=0.2,
        )

        prediction = model.predict(
            [19.0, 16.0, 15.0, 69.0, 87.0, 41.0]
        )

        self.assertIn(prediction, [1, -1])

    def test_empty_records(self):
        with self.assertRaises(ValueError):
            train_anomaly_model([])


if __name__ == "__main__":
    unittest.main()