import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


class TestAPI(unittest.TestCase):

    def test_health_check(self):
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "healthy"},
        )

    def test_analyze_valid_pgn(self):
        pgn = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0"

        response = client.post(
            "/analyze",
            json={"pgn": pgn},
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("anomaly_label", data)
        self.assertIn("isolation_score", data)
        self.assertIn("features", data)

        self.assertIn(
            "average_centipawn_loss",
            data["features"],
        )
        self.assertIn(
            "top1_agreement_percentage",
            data["features"],
        )
        self.assertIn(
            "top3_agreement_percentage",
            data["features"],
        )
        self.assertIn(
            "analyzed_move_count",
            data["features"],
        )

    def test_analyze_empty_pgn(self):
        response = client.post(
            "/analyze",
            json={"pgn": ""},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()