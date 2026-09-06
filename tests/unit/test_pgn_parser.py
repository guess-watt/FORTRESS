import unittest

from backend.app.pgn_parser import parse_pgn


class TestPGNParser(unittest.TestCase):

    def setUp(self):
        self.valid_pgn = """[Event "Test Game"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0"""

    def test_parse_valid_pgn(self):
        result = parse_pgn(self.valid_pgn)

        self.assertEqual(result["headers"]["Event"], "Test Game")
        self.assertEqual(result["headers"]["White"], "Player1")
        self.assertEqual(result["headers"]["Black"], "Player2")
        self.assertEqual(result["headers"]["Result"], "1-0")

    def test_extract_moves_as_uci(self):
        result = parse_pgn(self.valid_pgn)

        expected_moves = [
            "e2e4",
            "e7e5",
            "g1f3",
            "b8c6",
            "f1b5",
            "a7a6",
        ]

        self.assertEqual(result["moves"], expected_moves)

    def test_move_count(self):
        result = parse_pgn(self.valid_pgn)

        self.assertEqual(result["move_count"], 6)

    def test_empty_pgn(self):
        with self.assertRaises(ValueError):
            parse_pgn("")

    def test_pgn_with_no_moves(self):
        pgn = """[Event "Empty Game"]
[White "Player1"]
[Black "Player2"]
[Result "*"]"""

        with self.assertRaises(ValueError):
            parse_pgn(pgn)


if __name__ == "__main__":
    unittest.main()