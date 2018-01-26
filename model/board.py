# import numpy as np
import collections as ct
import tabulate as tb
from typing import List
from string import ascii_uppercase as cols

BLACK = "B"
WHITE = "W"
EMPTY = ' '
MARKS = '?!'


PseudoBoard = ct.namedtuple("PseudoBoard", ("w", "h", "board", "bool", "err"))

def tile_to_coords(t: str):
    return int(t[1]) - 1, cols.index(t[0]) - 1

class Tile:
    def __init__(self, color, x=None, y=None):
        self.color = color
        self.x, self.y = x, y

    def __repr__(self):
        return self.color

class Square:
    def __init__(self, x, y, tiles=None):
        self.x, self.y = x, y
        self.tiles = [] if tiles is None else tiles

    def add(self, tile: Tile):
        self.tiles.append(tile)
        tile.x, tile.y = self.x, self.y
        return self

    def extend(self, tiles: List[Tile]):
        self.tiles.extend(tiles)
        for tile in tiles:
            tile.x, tile.y = self.x, self.y
        return self

    def remove_top(self, n_tiles: int) -> List[Tile]:
        n = len(self.tiles) - n_tiles
        top = self.tiles[n:]
        self.tiles = self.tiles[:n]
        return top

    def copy(self):
        return Square(self.x, self.y, tiles=self.tiles[:])

    def __eq__(self, other):
        if other == EMPTY:
            return bool(self.tiles)
        return self.tiles == other.tiles

    def __repr__(self):
        return ''.join(str(t) for t in self.tiles)


class Board:
    def __init__(self, w: int, h: int, board = None):
        self.w, self.h = w, h
        self.board = [[Square(x, y) for x in range(w)]
                               for y in range(h)] if board is None else board

    """
    Attempt to place the tile.
    Returns a PseudoBoard object.
    
    @param tile
    @param x
    @param y
    @return nt was it placed?, board state
    """
    def place(self, tile: Tile, x: int, y: int):
        new_board = self.copy_board()
        if self.board[y][x] != EMPTY and \
                tile.x is None and tile.y is None:
            new_board[y][x].add(tile)
            return PseudoBoard(self.w, self.h, new_board, True, None)
        return PseudoBoard(self.w, self.h, new_board, False, "Tile cannot be placed there")

    """
    Move n_tiles from old_square to
    new_square. 
    """
    def move_single(self, old_square, new_square, n_tiles: int, first=False):
        if not isinstance(old_square, Square):
            old_square = self.get(*old_square)
        if not isinstance(new_square, Square):
            new_square = self.get(*new_square)

        new_board = self.copy_board()
        if abs(old_square.x - new_square.x == 1) ^ \
            abs(old_square.y - new_square.y == 1):
            if n_tiles <= len(old_square.tiles) - int(first):
                new_board[new_square.y][new_square.x] = new_square.copy()\
                    .extend(old_square.remove_top(n_tiles))
                new_board[old_square.y][old_square.x] = old_square.copy()
                return PseudoBoard(self.w, self.h, new_board, True, None)
        return PseudoBoard(self.w, self.h, new_board, False, "Tile cannot be moved")

    def force(self, pb: PseudoBoard):
        self.board = pb.board
        self.board = self.copy_board()

    def __repr__(self):
        return tb.tabulate(self.board, tablefmt="plain",
                           headers=list(range(1, self.w + 1)),
                           showindex=list(cols[:self.h]))

    def get(self, x:int, y:int) -> Square:
        return self.board[y][x]

    def copy_board(self):
        return [[s.copy()
                for s in r] for r in self.board]

b = Board(5, 5)
t = Tile(BLACK)
b.place(t, 1, 2)
b.force(b.place(Tile(WHITE), 1, 3))
b.force(b.move_single((1, 3), (1, 2), 1))
print(b)
