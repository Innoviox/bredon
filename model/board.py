# import numpy as np
import collections as ct
import tabulate as tb
from typing import List
from string import ascii_lowercase as cols

BLACK = "B"
WHITE = "W"
EMPTY = ' '
MARKS = '?!'

dirs = '+-<>'
UP, DOWN, LEFT, RIGHT = dirs
stones = 'FCS'
FLAT, CAP, STAND = stones

PseudoBoard = ct.namedtuple("PseudoBoard", ("w", "h", "board", "bool", "err"))

def tile_to_coords(t: str):
    return int(t[1]) - 1, cols.index(t[0])


class Tile:
    def __init__(self, color, stone='F', x=None, y=None):
        self.color, self.stone = color, stone
        self.x, self.y = x, y

    def __repr__(self):
        return '%s{%s}' % (self.color, self.stone)

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

    def next(self, dir):
        # TODO: checks on boundaries
        if dir == LEFT: # and self.y != 0:
            return self.x, self.y - 1
        if dir == RIGHT:
            return self.x, self.y + 1
        if dir == DOWN:
            return self.x - 1, self.y
        if dir == UP:
            return self.x + 1, self.y
        return "what"

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
            if isinstance(new_square, tuple):
                old_square = self.get(*old_square)
            elif isinstance(new_square, str):
                old_square = self.get(*tile_to_coords(old_square))
        if not isinstance(new_square, Square):
            if isinstance(new_square, tuple):
                new_square = self.get(*new_square)
            elif isinstance(new_square, str):
                new_square = self.get(*old_square.next(new_square))
            else:
                raise TypeError("new_square must be Square, tuple, or str, got: %s" % new_square.__class__)

        new_board = self.copy_board()
        if n_tiles <= len(old_square.tiles) - int(not first):
            valid = False
            flatten = False
            if len(new_square.tiles) == 0:
                valid = True
            else:
                new_stone = new_square.tiles[-1].stone
                old_stone = old_square.tiles[-1].stone
                if old_stone == CAP:
                    if new_stone == FLAT:
                        valid = True
                    elif new_stone == STAND and n_tiles == 1:
                        valid = True
                        flatten = True
                elif new_stone == FLAT:
                    valid = True
            if valid:
                new_board[new_square.y][new_square.x] = new_square.copy()\
                    .extend(old_square.remove_top(n_tiles))
                if flatten: new_square.tiles[-1].stone = FLAT

                new_board[old_square.y][old_square.x] = old_square.copy()
                return PseudoBoard(self.w, self.h, new_board, True, None)
            return PseudoBoard(self.w, self.h, new_board, False, f"Tile is not flat: stone == {new_square.tiles[-1].stone}")
        return PseudoBoard(self.w, self.h, new_board, False, f"Too many tiles: {n_tiles} > {len(old_square.tiles) - int(first)}")

    def move(self, old_square, dir, ns_tiles):
        first = True
        for n in ns_tiles:
            yield self.move_single(old_square, dir, n, first=first)
            first = False

    def parse_move(self, move, curr_player):
        move_dir = None
        for dir in dirs:
            if dir in move:
                move_dir = dir
                move = move.split(dir)
                break

        if move_dir == None:
            if len(move) == 2:
                move = 'F' + move
            return self.place(Tile(curr_player, stone=move[0]),
                              *tile_to_coords(move[1:]))

        else:
            # Move
            ns = move[1]

            t = move[0]
            if t[0] not in cols:
                ns += t[0]
                t = t[1:]

            if ns == '': ns = '1'
            ns = list(map(int, ns))
            return self.move(t, move_dir, ns)
        return "Not a valid move!"



    def force(self, pbs):
        if isinstance(pbs, PseudoBoard):
            self.force([pbs])
        else:
            for pb in pbs:
                if pb.err != None:
                    print('Error:', pb.err)
                else:
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

def load_moves_from_file(filename):
    with open(filename) as file:
        ptn = file.read().split("\n")
        size = int(ptn[4][7])
        b = Board(size, size)
        curr_player = WHITE
        for iturn, turn in enumerate(ptn[7:]):
            for imove, move in enumerate(turn.split(" ")[1:]): # Exclude the round number
                if iturn == 0:
                    curr_player = [BLACK, WHITE][imove]
                elif iturn == 1 and imove == 0:
                    curr_player = WHITE

                b.force(b.parse_move(move, curr_player))
                print(move)
                print(b)

                if curr_player == BLACK:
                    curr_player = WHITE
                else:
                    curr_player = BLACK
    return b

print(load_moves_from_file("/Users/chervjay/Documents/GitHub/Bredon/BeginnerBot vs rassar 18.1.26 11.42.ptn"))