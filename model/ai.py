from typing import List
import itertools as it
from operator import sub

from .board import Board, cols, tile_to_coords, coords_to_tile, EMPTY, dirs


def sums(n):
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in it.combinations(mid, i))
    return (list(map(sub, it.chain(s, e), it.chain(b, s))) for s in splits)

class StaticMoveAI(object):
    def __init__(self, board, curr_player):
        self.board = board
        self.curr_player = curr_player

    def generate_all_moves(self):
        for y in range(self.board.h):
            for x in range(self.board.w):
                s = coords_to_tile(x, y)
                tile = self.board.get(x, y)
                if tile == EMPTY:
                    yield s
                else:
                    # TODO: Check legality(?) of move strings
                    for direction in dirs:
                        # print(self.board)
                        # print(y, x)
                        # print("I am sure that tile does not equal empty.", tile == EMPTY)
                        # print(tile, direction, tile.next(direction), bool(tile.tiles), tile == EMPTY)
                        x1, y1 = tile.next(direction)
                        if 0 <= x1 < self.board.w and 0 <= y1 < self.board.h:
                            for i in range(1, len(tile.tiles) + 1):
                                if i == 1 and len(tile.tiles) == 1:
                                    yield s + direction
                                else:
                                    for move_amounts in sums(i):
                                        if len(move_amounts) == 1 and move_amounts[0] == i:
                                            yield str(i) + s + direction
                                        else:
                                            yield str(i) + s + direction + ''.join(map(str, move_amounts))

    def valid(self, move):
        return self.board.valid(self.board.parse_move(move, self.curr_player))

    def generate_valid_moves(self):
        return filter(self.valid, self.generate_all_moves())

    def pick_move(self):
        ...
