import unittest

from ml.models.anomaly_model import (
    AnomalyModel,
    prepare_features,
)


class TestAnomalyModel(unittest.TestCase):

    def setUp(self):
        self.features = {
            "average_centipawn_loss": 15.0,
            "top1_agreement_percentage": 70.0,
            "top3_agreement_percentage": 90.0,
            "analyzed_move_count": 40,
        }

    def test_prepare_features(self):
        result = prepare_features(self.features)

        self.assertEqual(
            result,
            [15.0, 70.0, 90.0, 40.0],
        )

    def test_missing_features(self):
        incomplete_features = {
            "average_centipawn_loss": 15.0,
        }

        with self.assertRaises(ValueError):
            prepare_features(incomplete_features)

    def test_model_training(self):
        training_data = [
            [15.0, 70.0, 90.0, 40.0],
            [20.0, 65.0, 85.0, 35.0],
            [25.0, 60.0, 80.0, 45.0],
            [18.0, 72.0, 88.0, 50.0],
            [22.0, 68.0, 82.0, 42.0],
        ]

        model = AnomalyModel()
        result = model.fit(training_data)

        self.assertIs(result, model)

    def test_prediction(self):
        training_data = [
            [15.0, 70.0, 90.0, 40.0],
            [20.0, 65.0, 85.0, 35.0],
            [25.0, 60.0, 80.0, 45.0],
            [18.0, 72.0, 88.0, 50.0],
            [22.0, 68.0, 82.0, 42.0],
        ]

        model = AnomalyModel()
        model.fit(training_data)

        prediction = model.predict(
            [19.0, 69.0, 87.0, 41.0]
        )

        self.assertIn(prediction, [1, -1])

    def test_anomaly_score(self):
        training_data = [
            [15.0, 70.0, 90.0, 40.0],
            [20.0, 65.0, 85.0, 35.0],
            [25.0, 60.0, 80.0, 45.0],
            [18.0, 72.0, 88.0, 50.0],
            [22.0, 68.0, 82.0, 42.0],
        ]

        model = AnomalyModel()
        model.fit(training_data)

        score = model.anomaly_score(
            [19.0, 69.0, 87.0, 41.0]
        )

        self.assertIsInstance(score, float)

    def test_empty_training_data(self):
        model = AnomalyModel()

        with self.assertRaises(ValueError):
            model.fit([])


if __name__ == "__main__":
    unittest.main()