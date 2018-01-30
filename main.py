from model.board import load_moves_from_file, WHITE
from model.ai import StaticMoveAI

board = load_moves_from_file("You vs You 18.1.29 20.43.ptn")
print(board)
ai = StaticMoveAI(board, WHITE)
for m in ai.generate_valid_moves():
    print(ai.board)
    print(board)
    print(m)