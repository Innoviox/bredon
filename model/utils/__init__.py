import numpy as np
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

PseudoBoard = ct.namedtuple("PseudoBoard", ("w", "h", "board", "bool", "err", "type"))

sizes = {
    3: [10, 0],
    4: [15, 0],
    5: [21, 1],
    6: [30, 1],
    7: [40, 2],
    8: [50, 2]
}


def tile_to_coords(t: str):
    return int(t[1]) - 1, cols.index(t[0])


def coords_to_tile(x: int, y: int):
    return cols[y] + str(x + 1)


def next(obj, direction):
    # TODO: checks on boundaries
    if hasattr(obj, 'x') and hasattr(obj, 'y'):
        if direction == LEFT:  # and self.y != 0:
            return obj.x, obj.y - 1
        if direction == RIGHT:
            return obj.x, obj.y + 1
        if direction == DOWN:
            return obj.x - 1, obj.y
        if direction == UP:
            return obj.x + 1, obj.y
    raise TypeError("Object must have an x and y attribute")


class Tile:
    def __init__(self, color, stone='F', x=None, y=None):
        self.color, self.stone = color, stone
        self.x, self.y = x, y

    def next(self, direction):
        return next(self, direction)

    def __repr__(self):
        return '%s{%s}' % (self.color, self.stone)  # + f'@{coords_to_tile(self.x, self.y)}'

    def __eq__(self, other):
        if isinstance(other, Tile):
            return (self.color, self.stone, self.x, self.y) == \
                   (other.color, other.stone, other.x, other.y)
        elif isinstance(other, Square):
            return other.tiles and self == other.tiles[-1]
        elif isinstance(other, tuple):
            return (self.color, self.stone) == tuple
        return False


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
        return Square(self.x, self.y, tiles=[Tile(t.color, stone=t.stone, x=t.x, y=t.y) for t in self.tiles])

    def next(self, direction):
        return next(self, direction)

    def __eq__(self, other):
        if other == EMPTY:
            return not bool(self.tiles)
        if isinstance(other, Square):
            return self.tiles == other.tiles
        if isinstance(other, Tile) and self.tiles:
            return self.tiles[-1] == other
        return False

    def __repr__(self):
        return ''.join(str(t) for t in self.tiles)  # + f'@{coords_to_tile(self.x, self.y)}'


class Board:
    def __init__(self, w: int, h: int, board=None):
        self.w, self.h = w, h
        self.board = [[Square(x, y) for x in range(w)]
                      for y in range(h)] if board is None else board
        self.stones, self.caps = sizes[w]

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
        if self.board[y][x] == EMPTY and \
                tile.x is None and tile.y is None:
            new_board[y][x].add(tile)
            return PseudoBoard(self.w, self.h, new_board, True, None, "place")
        return PseudoBoard(self.w, self.h, new_board, False, "Tile cannot be placed there", None)

    """
    Move n_tiles from old_square to
    new_square. 
    """

    def move_single(self, old_square, new_square, n_tiles: int, first=False):
        # print("Verbose running of move_single with args:", old_square, new_square, n_tiles, first)
        # print("Board state:", self.board)
        if not isinstance(old_square, Square):
            if isinstance(new_square, tuple):
                old_square = self.get(*old_square)  # .copy()
            elif isinstance(new_square, str):
                old_square = self.get(*tile_to_coords(old_square))  # .copy()
        else:
            old_square = self.get(old_square.x, old_square.y)

        if not isinstance(new_square, Square):
            if isinstance(new_square, tuple):
                new_square = self.get(*new_square)  # .copy()
            elif isinstance(new_square, str):
                new_square = self.get(*old_square.next(new_square))  # .copy()
            else:
                raise TypeError("new_square must be Square, tuple, or str, got: %s" % new_square.__class__)
        else:
            new_square = self.get(new_square.x, new_square.y)

        new_square = new_square.copy()
        old_square = old_square.copy()
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
                new_board[new_square.y][new_square.x] = new_square.copy() \
                    .extend(old_square.remove_top(n_tiles))
                if flatten:
                    new_square.tiles[-1].stone = FLAT

                new_board[old_square.y][old_square.x] = old_square.copy()
                return PseudoBoard(self.w, self.h, new_board, True, None, "move")
            return PseudoBoard(self.w, self.h, new_board, False,
                               f"Tile is not flat: stone == {new_square.tiles[-1].stone}", None)
        return PseudoBoard(self.w, self.h, new_board, False,
                           f"Too many tiles: {n_tiles} > {len(old_square.tiles) - int(not first)}", None)

    def move(self, old_square, direction, ns_moves, ns_total):
        def _run(fn):
            try:
                pb = fn()
                copy.force(pb)
                return pb
            except IndexError as e:
                return PseudoBoard(self.w, self.h, [], False, e, None)

        copy = self.copy()
        sq = copy.get(*tile_to_coords(old_square))
        yield _run(lambda: copy.move_single(sq, direction, ns_total, first=True))
        for n in range(1, len(ns_moves)):
            sq = copy.get(*sq.next(direction))
            yield _run(lambda: copy.move_single(sq, direction, sum(ns_moves[n:]), first=False))

    def parse_move(self, move, curr_player):
        move_dir = None
        for direction in dirs:
            if direction in move:
                move_dir = direction
                move = move.split(direction)
                break

        if move_dir is None:
            if len(move) == 2:
                move = 'F' + move
            return self.place(Tile(curr_player, stone=move[0]),
                              *tile_to_coords(move[1:]))

        else:
            # Move
            ns = move[1]

            t = move[0]
            if t[0] not in cols:
                total = int(t[0])
                t = t[1:]
            else:
                total = 1

            return self.move(t, move_dir, list(map(int, ns)), total)

    def force(self, pbs):
        if isinstance(pbs, PseudoBoard):
            self.force([pbs])
        else:
            for pb in pbs:
                if pb.err is not None:
                    # print('Error:', pb.err)
                    return pb.err
                else:
                    # print("Confirmed move", pb)
                    # print(self.board)
                    self.board = pb.board
                    # print(self.board)
                    # self.board = self.copy_board()

    def force_str(self, s, curr_player):
        return self.force(self.parse_move(s, curr_player))

    def valid(self, pbs):
        new_board = self.copy()
        return new_board.force(pbs) is None
        # if isinstance(pbs, PseudoBoard):
        #     return self.valid([pbs])
        # try:

        #     if
        #      return True
        # except IndexError:
        #     return False
        # return all(i.err is None for i in pbs)

    def winner(self, players):
        r = self.road()
        if r:
            return r
        elif all(sq != EMPTY for row in self.board for sq in row) or \
                any(player.out_of_tiles() for player in players):
            return self.flat_win()
        return None

    def flat_win(self):
        def _sum(color):
            return sum(1 for row in self.board for sq in row if sq.tiles and sq.tiles[-1] == (color, FLAT))

        w, b = _sum(WHITE), _sum(BLACK)
        return False if w == b else WHITE if w > b else BLACK

    def road(self) -> bool:
        new_board = np.array(self.copy_board())
        for r, row in enumerate(new_board):
            for c, col in enumerate(row):
                if col.tiles:
                    tile = col.tiles[-1]
                    new_board[r, c] = tile if tile.stone in [FLAT, CAP] else None
                else:
                    new_board[r, c] = None
        for board in (new_board, new_board.T):
            for tile in board[0]:
                if tile is not None:
                    conns = self.get_connections(tile, tile, new_board, [])
                    if conns[-1].y - conns[0].y == self.h - 1 or \
                            conns[-1].x - conns[0].x == self.w - 1:
                        return tile.color
        return False

    def get_connections(self, tile: Tile, origtile: Tile, board, tiles) -> List[Tile]:
        if tile is None: return []
        tiles.append(tile)
        conns = [tile]
        for dir in dirs:
            try:
                x, y = tile.next(dir)
                if 0 <= x < self.w and 0 <= y < self.h:
                    t = board[y, x]
                    if t != origtile and t not in conns and t not in tiles and t.color == origtile.color:
                        conns.extend(self.get_connections(t, origtile, board, tiles))
                    else:
                        pass
            except IndexError as e:
                pass  # print(e)
            except AttributeError as e:
                pass  # print(e)
        return conns

    def get(self, x: int, y: int) -> Square:
        return self.board[y][x]

    def copy_board(self):
        return [[s.copy()
                 for s in r] for r in self.board]

    def copy(self):
        return Board(self.w, self.h, board=self.copy_board())

    def __repr__(self):
        return tb.tabulate(self.board, tablefmt="plain",
                           headers=list(range(1, self.w + 1)),
                           showindex=list(cols[:self.h]))


def load_moves_from_file(filename):
    with open(filename) as file:
        ptn = file.read().split("\n")
        size = int(ptn[4][7])
        b = Board(size, size)
        curr_player = WHITE
        for iturn, turn in enumerate(ptn[7:]):
            if 'R' in turn:
                break
            for imove, move in enumerate(turn.split(" ")[1:]):  # Exclude the round number
                if move:
                    if iturn == 0:
                        curr_player = [BLACK, WHITE][imove]
                    elif iturn == 1 and imove == 0:
                        curr_player = WHITE

                    # print(move)
                    b.force(b.parse_move(move, curr_player))

                    # print(b)
                    # print("Road?:", b.road())

                    if curr_player == BLACK:
                        curr_player = WHITE
                    else:
                        curr_player = BLACK
    return b  # , turn


# print(load_moves_from_file("/Users/chervjay/Documents/GitHub/Bredon/BeginnerBot vs rassar 18.1.26 11.42.ptn"))
# print(load_moves_from_file("/Users/chervjay/Documents/GitHub/Bredon/You vs You 18.1.26 15.42.ptn"))
# print(load_moves_from_file("rassar vs IntuitionBot 18.1.26 21.40.ptn"))

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

    def out_of_tiles(self):
        return self.caps > self.board.caps and self.stones > self.board.stones
