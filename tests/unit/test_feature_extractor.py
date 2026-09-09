import unittest

from backend.app.feature_extractor import extract_features


class TestFeatureExtractor(unittest.TestCase):

    def test_empty_results(self):
        with self.assertRaises(ValueError):
            extract_features([])

    def test_average_centipawn_loss(self):
        results = [
            {"centipawn_loss": 10, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 20, "engine_rank": 2, "engine_agreement": True},
            {"centipawn_loss": 30, "engine_rank": 3, "engine_agreement": True},
            {"centipawn_loss": 40, "engine_rank": 1, "engine_agreement": True},
        ]

        features = extract_features(results)

        self.assertEqual(
            features["average_centipawn_loss"],
            25.0,
        )

    def test_top1_agreement_percentage(self):
        results = [
            {"centipawn_loss": 10, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 20, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 30, "engine_rank": 2, "engine_agreement": True},
            {"centipawn_loss": 40, "engine_rank": 3, "engine_agreement": True},
        ]

        features = extract_features(results)

        self.assertEqual(
            features["top1_agreement_percentage"],
            50.0,
        )


    def test_top3_agreement_percentage(self):
        results = [
            {"centipawn_loss": 10, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 20, "engine_rank": 2, "engine_agreement": True},
            {"centipawn_loss": 30, "engine_rank": 3, "engine_agreement": True},
            {"centipawn_loss": 40, "engine_rank": None, "engine_agreement": False},
        ]

        features = extract_features(results)

        self.assertEqual(
            features["top3_agreement_percentage"],
            75.0,
        )


    def test_analyzed_move_count(self):
        results = [
            {"centipawn_loss": 10, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 20, "engine_rank": 2, "engine_agreement": True},
            {"centipawn_loss": 30, "engine_rank": 3, "engine_agreement": True},
            {"centipawn_loss": 40, "engine_rank": None, "engine_agreement": False},
            {"centipawn_loss": 15, "engine_rank": 1, "engine_agreement": True},
        ]

        features = extract_features(results)

        self.assertEqual(
            features["analyzed_move_count"],
            5,
        )

    def test_game_summary_features(self):
        results = [
            {"centipawn_loss": 10, "engine_rank": 1, "engine_agreement": True},
            {"centipawn_loss": 20, "engine_rank": 2, "engine_agreement": True},
            {"centipawn_loss": 30, "engine_rank": 3, "engine_agreement": True},
            {"centipawn_loss": 40, "engine_rank": None, "engine_agreement": False},
        ]

        features = extract_features(results)

        self.assertEqual(features["analyzed_move_count"], 4)
        self.assertEqual(features["average_centipawn_loss"], 25.0)
        self.assertEqual(features["top1_agreement_percentage"], 25.0)
        self.assertEqual(features["top3_agreement_percentage"], 75.0)


if __name__ == "__main__":
    unittest.main()