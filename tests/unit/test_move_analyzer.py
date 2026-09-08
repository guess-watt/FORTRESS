import unittest

from backend.app.pgn_parser import parse_pgn
from backend.app.move_analyzer import (
    analyze_game,
    calculate_engine_agreement_percentage,
    calculate_average_centipawn_loss,
    calculate_top1_agreement_percentage,
    calculate_analyzed_move_count,
    calculate_game_summary,
)


class TestMoveAnalyzer(unittest.TestCase):

    def test_empty_moves(self):
        with self.assertRaises(ValueError):
            analyze_game([])

    def test_illegal_move(self):
        moves = ["e2e5"]

        with self.assertRaises(ValueError):
            analyze_game(moves)

    def test_analyze_game(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
            "b8c6",
            "f1b5",
            "a7a6",
        ]

        results = analyze_game(moves)

        self.assertEqual(len(results), 6)

    def test_player_assignment(self):
        moves = [
            "e2e4",
            "e7e5",
        ]

        results = analyze_game(moves)

        self.assertEqual(results[0]["player"], "White")
        self.assertEqual(results[1]["player"], "Black")

    def test_move_numbers(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
            "b8c6",
        ]

        results = analyze_game(moves)

        self.assertEqual(results[0]["move_number"], 1)
        self.assertEqual(results[1]["move_number"], 1)
        self.assertEqual(results[2]["move_number"], 2)
        self.assertEqual(results[3]["move_number"], 2)

    def test_analysis_fields(self):
        moves = ["e2e4"]

        result = analyze_game(moves)[0]

        self.assertIn("played_move", result)
        self.assertIn("best_move", result)
        self.assertIn("evaluation_before", result)
        self.assertIn("evaluation_after", result)
        self.assertIn("centipawn_loss", result)

    def test_centipawn_loss_is_non_negative(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
        ]

        results = analyze_game(moves)

        for result in results:
            self.assertGreaterEqual(
                result["centipawn_loss"],
                0,
            )

    def test_engine_rank(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
        ]

        results = analyze_game(moves)

        for result in results:
            self.assertIn("engine_rank", result)
            self.assertIn("top_engine_moves", result)
            self.assertGreaterEqual(result["engine_rank"], 1)
            self.assertLessEqual(
                result["engine_rank"],
                len(result["top_engine_moves"]),
            )

    def test_engine_rank_can_be_non_best(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
            "b8c6",
            "f1b5",
            "a7a6",
            "b5a4",
            "g8f6",
            "e1g1",
            "f8e7",
            "f1e1",
            "d7d6",
            "a2a3",
        ]

        results = analyze_game(moves)

        non_best_results = [
            result
            for result in results
            if result["engine_rank"] > 1
        ]

        self.assertGreater(len(non_best_results), 0)

    def test_pgn_to_move_analysis_pipeline(self):
        pgn = """[Event "Integration Test"]
[Site "Local"]
[Date "2026.09.09"]
[Round "1"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0"""

        game = parse_pgn(pgn)
        results = analyze_game(game["moves"])

        self.assertEqual(game["move_count"], 6)
        self.assertEqual(len(results), 6)

        for result in results:
            self.assertIn("played_move", result)
            self.assertIn("best_move", result)
            self.assertIn("top_engine_moves", result)
            self.assertIn("engine_rank", result)
            self.assertIn("centipawn_loss", result)


    def test_engine_agreement(self):
        moves = [
            "e2e4",
            "e7e5",
            "g1f3",
        ]

        results = analyze_game(moves)

        for result in results:
            self.assertIn("engine_agreement", result)
            self.assertIsInstance(
                result["engine_agreement"],
                bool,
            )

            if result["engine_rank"] is not None:
                self.assertTrue(result["engine_agreement"])
            else:
                self.assertFalse(result["engine_agreement"])

    def test_engine_agreement_percentage(self):
        results = [
            {"engine_agreement": True},
            {"engine_agreement": True},
            {"engine_agreement": False},
            {"engine_agreement": True},
        ]

        percentage = calculate_engine_agreement_percentage(results)

        self.assertEqual(percentage, 75.0)

    def test_engine_agreement_percentage_empty(self):
        percentage = calculate_engine_agreement_percentage([])

        self.assertEqual(percentage, 0.0)

    def test_average_centipawn_loss(self):
        results = [
            {"centipawn_loss": 10},
            {"centipawn_loss": 20},
            {"centipawn_loss": 30},
            {"centipawn_loss": 40},
        ]

        average = calculate_average_centipawn_loss(results)

        self.assertEqual(average, 25.0)


    def test_average_centipawn_loss_empty(self):
        average = calculate_average_centipawn_loss([])

        self.assertEqual(average, 0.0)

    def test_top1_agreement_percentage(self):
        results = [
            {"engine_rank": 1},
            {"engine_rank": 1},
            {"engine_rank": 2},
            {"engine_rank": 3},
        ]

        percentage = calculate_top1_agreement_percentage(results)

        self.assertEqual(percentage, 50.0)


    def test_top1_agreement_percentage_empty(self):
        percentage = calculate_top1_agreement_percentage([])

        self.assertEqual(percentage, 0.0)

    def test_analyzed_move_count(self):
        results = [
            {"centipawn_loss": 10},
            {"centipawn_loss": 20},
            {"centipawn_loss": 30},
        ]

        count = calculate_analyzed_move_count(results)

        self.assertEqual(count, 3)


    def test_analyzed_move_count_empty(self):
        count = calculate_analyzed_move_count([])

        self.assertEqual(count, 0)

    def test_game_summary(self):
        results = [
            {
                "centipawn_loss": 10,
                "engine_rank": 1,
                "engine_agreement": True,
            },
            {
                "centipawn_loss": 20,
                "engine_rank": 1,
                "engine_agreement": True,
            },
            {
                "centipawn_loss": 30,
                "engine_rank": 2,
                "engine_agreement": True,
            },
            {
                "centipawn_loss": 40,
                "engine_rank": None,
                "engine_agreement": False,
            },
        ]

        summary = calculate_game_summary(results)

        self.assertEqual(summary["move_count"], 4)
        self.assertEqual(summary["average_centipawn_loss"], 25.0)
        self.assertEqual(summary["top1_agreement_percentage"], 50.0)
        self.assertEqual(summary["top3_agreement_percentage"], 75.0)

    def test_game_summary_empty(self):
        summary = calculate_game_summary([])

        self.assertEqual(summary["move_count"], 0)
        self.assertEqual(summary["average_centipawn_loss"], 0.0)
        self.assertEqual(summary["top1_agreement_percentage"], 0.0)
        self.assertEqual(summary["top3_agreement_percentage"], 0.0)

if __name__ == "__main__":
    unittest.main()