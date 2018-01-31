from .board import *

class Player(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.stones, self.caps = 0, 0

    def do(self, m):
        move = self.board.parse_move(m, self.color)
        if isinstance(move, PseudoBoard):
            if move.bool:
                stone_type = FLAT if len(m) == 2 else m[0]
                stone, cap = False, False
                if stone_type in [FLAT, STAND]:
                    self.stones += 1
                    stone = True
                else:
                    self.caps += 1
                    cap = True
                caps, stones = self.caps > self.board.caps, self.stones > self.board.stones
                if stones and caps:
                    self.stones -= stone
                    self.caps -= cap
                    # TODO: End the game
                    self.board.end_game()
                elif (stones and stone) or (caps and cap):
                    self.stones -= stone
                    self.caps -= cap
                    raise ValueError(f"Not enough pieces left")
                                     # f"\tStones played: {self.stones}, Total: {self.board.stones}"
                                     # f"\tCaps played: {self.caps}, Total: {self.board.caps}"
                                     # f"Stone: {stone}, Cap: {cap}")
                else:
                    self.board.force(move)
            else:
                # Move is illegal
                raise ValueError("Illegal Move")
        else:
            self.board.force(move)

