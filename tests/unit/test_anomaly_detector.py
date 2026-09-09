import unittest

from backend.app.anomaly_detector import (
    calculate_anomaly_score,
    get_anomaly_reasons,
)


class TestAnomalyDetector(unittest.TestCase):

    def test_missing_features(self):
        with self.assertRaises(ValueError):
            calculate_anomaly_score({})

    def test_zero_analyzed_moves(self):
        features = {
            "average_centipawn_loss": 10,
            "top1_agreement_percentage": 80,
            "top3_agreement_percentage": 95,
            "analyzed_move_count": 0,
        }

        with self.assertRaises(ValueError):
            calculate_anomaly_score(features)

    def test_score_is_zero_for_normal_features(self):
        features = {
            "average_centipawn_loss": 50,
            "top1_agreement_percentage": 30,
            "top3_agreement_percentage": 60,
            "analyzed_move_count": 40,
        }

        score = calculate_anomaly_score(features)

        self.assertEqual(score, 0.0)

    def test_score_increases_for_anomalous_features(self):
        features = {
            "average_centipawn_loss": 10,
            "top1_agreement_percentage": 80,
            "top3_agreement_percentage": 95,
            "analyzed_move_count": 40,
        }

        score = calculate_anomaly_score(features)

        self.assertEqual(score, 90.0)

    def test_score_cannot_exceed_100(self):
        features = {
            "average_centipawn_loss": 1,
            "top1_agreement_percentage": 100,
            "top3_agreement_percentage": 100,
            "analyzed_move_count": 40,
        }

        score = calculate_anomaly_score(features)

        self.assertLessEqual(score, 100.0)

    def test_reasons_for_anomalous_features(self):
        features = {
            "average_centipawn_loss": 10,
            "top1_agreement_percentage": 80,
            "top3_agreement_percentage": 95,
            "analyzed_move_count": 40,
        }

        reasons = get_anomaly_reasons(features)

        self.assertEqual(len(reasons), 3)

    def test_no_reasons_for_normal_features(self):
        features = {
            "average_centipawn_loss": 50,
            "top1_agreement_percentage": 30,
            "top3_agreement_percentage": 60,
            "analyzed_move_count": 40,
        }

        reasons = get_anomaly_reasons(features)

        self.assertEqual(reasons, [])


if __name__ == "__main__":
    unittest.main()