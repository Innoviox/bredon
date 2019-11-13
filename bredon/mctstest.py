from .model import *

board = Board(size=5)
human = Player(board, Colors.WHITE)
ai = MonteAI(5, Colors.BLACK)

while 1:
