import unittest
from model import *

class TestAI(unittest.TestCase):
    def test_block(self):
        b = Board(4)
        for move in ["a1", "a2", "a3"]:
            b.force_str(move, Colors.WHITE)
        ai = MinimaxAI(b, Colors.BLACK)
        self.assertEqual(str(ai.pick_move(4)), "a4", "Error: AI did not block road threat A")

    def test_take(self):
        b = Board(4)
        for move in ["a1", "a2", "a3"]:
            b.force_str(move, Colors.WHITE)
        ai = MinimaxAI(b, Colors.WHITE)
        self.assertEqual(str(ai.pick_move(4)), "a4", "Error: AI did not take road threat A")

if __name__ == '__main__':
    unittest.main()