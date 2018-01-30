from model.board import Board, load_moves_from_file
from model.ai import StaticMoveAI

board = load_moves_from_file("You vs You 18.1.29 20.43.ptn")
print(board)
for m in StaticMoveAI(board).generate_all_moves():
    print(m)