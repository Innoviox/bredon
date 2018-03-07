from .const import *


@dc.dataclass
class Move:
    total: int = 1
    stone: str = FLAT
    col: str = None
    row: int = None
    moves: list = dc.field(default_factory=list)
    direction: str = None

    def get_square(self):
        return self.col + str(self.row)

    def __repr__(self):
        return 'Move(' + ', '.join([f"{k}={v!r}" for k, v in self.__dict__.items()]) + ')'

    def __str__(self):
        if not self.direction:
            return (self.stone + self.get_square()).strip(FLAT)
        else:
            return str(self.total) + self.get_square() + self.direction + ''.join(map(str, self.moves))


@dc.dataclass
class Tile(Next):
    color: str
    stone: str = FLAT
    x: int = None
    y: int = None

    def __repr__(self):
        return '%s{%s}' % (self.color, self.stone)  # + f'@{coords_to_tile(self.x, self.y)}'


class Square(Next):
    def __init__(self, x, y, tiles=None):
        self.x, self.y = x, y
        self.tiles = [] if tiles is None else tiles

    def fix(self, tile):
        tile.x, tile.y = self.x, self.y

    def add(self, tile: Tile):
        self.tiles.append(tile)
        self.fix(tile)
        return self

    def extend(self, tiles):
        for tile in tiles:
            self.fix(tile)
        self.tiles.extend(tiles)
        return self

    def remove_top(self, n_tiles: int):
        n = len(self.tiles) - n_tiles
        top = self.tiles[n:]
        self.tiles = self.tiles[:n]
        return top

    def connections(self, board):
        conns = 0
        s = len(board)
        for direction in dirs:
            x, y = self.next(direction, s)
            t_next = board[y][x].tiles
            if t_next:
                t_next = t_next[-1]
                t = self.tiles
                if t:
                    t = t[-1]
                    if t_next is not t and \
                            t_next.color == t.color and t_next.stone in 'FC' and t.stone in 'FC':
                        conns += 1
        return conns

    def copy(self):
        return Square(self.x, self.y, tiles=self.tiles[:])

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
    def __init__(self, size: int, board=None):
        self.size = size
        self.board = np.array([[Square(x, y) for x in range(size)]
                              for y in range(size)]) if board is None else board
        self.stones, self.caps = sizes[size]

    def place(self, move: Move, curr_player):
        """
        Attempt to place the tile.
        Returns a PseudoBoard object.

        :param move
        :param curr_player
        :return nt was it placed?, board state
        """
        tile = Tile(curr_player, stone=move.stone)
        x, y = tile_to_coords(move.get_square())
        new_board = self.copy_board()
        if self.board[y][x] == EMPTY and \
                tile.x is None and tile.y is None:
            new_board[y][x].add(tile)
            return PseudoBoard(self.size, self.size, new_board, True, None, "place")
        return PseudoBoard(self.size, self.size, new_board, False, "Tile cannot be placed there", None)

    def move_single(self, old_square, new_square, n_tiles: int, first=False):
        """
        Move n_tiles from old_square to
        new_square.
        """
        if not isinstance(old_square, Square):
            if isinstance(new_square, tuple):
                old_square = self.get(*old_square)
            elif isinstance(new_square, str):
                old_square = self.get(*tile_to_coords(old_square))
        else:
            old_square = self.get(old_square.x, old_square.y)

        if not isinstance(new_square, Square):
            if isinstance(new_square, tuple):
                new_square = self.get(*new_square)
            elif isinstance(new_square, str):
                try:
                    new_square = self.get(*old_square.next(new_square, SIZE))
                except ValueError:
                    return PseudoBoard(self.size, self.size, self.board, False,
                                       f"{old_square.x}, {old_square.y} is out of bounds for {new_square}", None)
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
                return PseudoBoard(self.size, self.size, new_board, True, None, "move")
            return PseudoBoard(self.size, self.size, new_board, False,
                               f"Tile is not flat: stone == {new_square.tiles[-1].stone}", None)
        return PseudoBoard(self.size, self.size, new_board, False,
                           f"Too many tiles: {n_tiles} > {len(old_square.tiles) - int(not first)}", None)

    def move(self, move: Move):
        copy = self.copy()
        sq = copy.get(*tile_to_coords(move.get_square()))
        yield self._run(lambda: copy.move_single(sq, move.direction, move.total, first=True), copy)
        for n in range(1, len(move.moves)):
            sq = copy.get(*sq.next(move.direction, self.size))
            yield self._run(lambda: copy.move_single(sq, move.direction, sum(move.moves[n:]), first=False), copy)

    def parse_move(self, move: Move, curr_player):
        if move.direction is None:
            return self.place(move, curr_player)
        else:
            return self.move(move)

    def force(self, pbs):
        if isinstance(pbs, PseudoBoard):
            self.force([pbs])
        else:
            new_board = self.copy_board()
            for pb in pbs:
                if pb.err is not None:
                    return pb.err
                else:
                    new_board = pb.board
            self.board = new_board

    def force_move(self, s, curr_player):
        return self.force(self.parse_move(s, curr_player))

    def force_str(self, s, curr_player):
        return self.force(self.parse_move(str_to_move(s), curr_player))

    def valid(self, pbs):
        new_board = self.copy()
        return new_board.force(pbs) is None

    def valid_move(self, move, color):
        new_board = self.copy()
        return new_board.force_move(move, color) is None

    def winner(self, players, t=False):
        r = self.road()
        if r:
            return r
        elif all(sq != EMPTY for row in self.board for sq in row) or \
                any(player.out_of_tiles() for player in players):
            return self.flat_win(t=t, f=True)
        return None

    def flat_win(self, t=False, f=False):
        w, b = self._sum(WHITE), self._sum(BLACK)
        if f or all(len(sq.tiles) > 0 for row in self.board for sq in row):
            return ("TIE" if t else False) if w == b else WHITE if w > b else BLACK
        return False

    def road(self):
        for board, xy in zip((self.board, np.transpose(self.board)), (False, True)):
            for color in COLORS:
                if self._road_check(color, board, xy=xy):
                    return color
        return False

    def compress_left(self, color, board, xy):
        return list(it.starmap(fc.partial(self._cl_row_check, color, xy, board), enumerate(board)))
      
    def get(self, x: int, y: int) -> Square:
        return self.board[y][x]

    def copy_board(self):
        return np.array([list(map(Square.copy, r)) for r in self.board])

    def copy(self):
        return Board(self.size, board=self.copy_board())

    def __repr__(self):
        return tb.tabulate(self.board,
                           tablefmt="plain",
                           headers=list(range(1, self.size + 1)),
                           showindex=list(cols[:self.size]))

    def evaluate(self, color):
        return self._evaluate(color) - self._evaluate(flip_color(color)) * 2

    def execute(self, move, color):
        self.force_move(move, color)

    def set(self, old_state):
        self.board = old_state

    def _valid(self, move, color):
        return self.valid(self.parse_move(move, color))

    def generate_valid_moves(self, color, caps):
        return filter(lambda move: self._valid(move, color), self.generate_all_moves(color, caps))

    def generate_all_moves(self, color, caps):
        for y in range(self.size):
            for x in range(self.size):
                c, r = coords_to_tile(x, y)
                tile = self.get(x, y)
                if tile == EMPTY:
                    for stone in FLAT + STAND:
                        yield Move(stone=stone, col=c, row=r)
                    if caps < self.caps:
                        yield Move(stone=CAP, col=c, row=r)
                else:
                    if tile.tiles[-1].color == color:
                        for direction in dirs:
                            try:
                                x1, y1 = tile.next(direction, SIZE)
                                if 0 <= x1 < self.size and 0 <= y1 < self.size:
                                    for i in range(1, min(len(tile.tiles) + 1, self.size + 1)):
                                        if i == 1 and len(tile.tiles) == 1:
                                            yield Move(col=c, row=r, direction=direction)
                                        else:
                                            for moves in sums(i):
                                                if len(moves) == 1 and moves[0] == i:
                                                    yield Move(total=i, col=c, row=r, direction=direction)
                                                else:
                                                    yield Move(total=i, col=c, row=r, moves=moves, direction=direction)
                            except ValueError:
                                pass

    # STATIC PRIVATE HELPER METHODS
    def _run(self, fn, copy):
        try:
            pb = fn()
            copy.force(pb)
            return pb
        except IndexError as e:
            return PseudoBoard(self.size, self.size, [], False, e, None)

    def _evaluate_sq(self, color, sq):
        e = 0
        if sq.tiles:
            t = sq.tiles[-1]
            if t.color == color:
                e += sum(1 for i in sq.tiles if i.color == color and i.stone in 'CF') ** 1.5
                e += (sq.connections(self.board) + 1) ** 2
        return e

    def _evaluate(self, color):
        return sum(map(fc.partial(self._evaluate_sq, color), self.board.ravel('C')))

    def _cl_sq_check(self, r, color, board, xy, sq):
        if sq.tiles and sq.tiles[-1].color == color:
            conns = sq.connections(board)
            return conns > 1 or ((r == 0 or r == self.size - 1) and conns > 0)
        return False

    def _cl_row_check(self, color, xy, board, r, row):
        return list(filter(fc.partial(self._cl_sq_check, r, color, board, xy), row))

    def _sum(self, color):
        return sum(1 for row in self.board for sq in row if sq.tiles and
                   sq.tiles[-1].color == color and sq.tiles[-1].stone == FLAT)

    def _road_check(self, color, board, xy):
        road = self.compress_left(color, board, xy)
        if all(road) or \
                any(len(road[i]) >= self.size for i in range(self.size)):
            return color
        return False


class Player(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.stones, self.caps = 0, 0

    def _do(self, m: Move, c):
        move = self.board.parse_move(m, c)
        if isinstance(move, PseudoBoard):
            if move.bool:
                stone_type = m.stone
                stone, cap = False, False
                if stone_type in [FLAT, STAND]:
                    self.stones += 1
                    stone = True
                else:
                    self.caps += 1
                    cap = True
                caps, _stones = self.caps > self.board.caps, self.stones > self.board.stones
                if _stones and caps:
                    self.stones -= stone
                    self.caps -= cap
                    # TODO: End the game
                    self.board.end_game()
                elif (_stones and stone) or (caps and cap):
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

    def do(self, m: Move):
        return self._do(m, self.color)

    def out_of_tiles(self):
        return self.caps >= self.board.caps and self.stones >= self.board.stones

    def _pick_move(self, color):
        while True:
            m = str_to_move(input("Enter move: "))
            try:
                v = self.board.valid_move(m, color)
                if v:
                    return m, color
                else:
                    print("Parsed move", m)
                    print("Received error", v)
            except Exception as e:
                print("Parsed move", m)
                print("Received error", e)

    def pick_move(self):
        return self._pick_move(self.color)

    def pick_opposing_move(self):
        return self._pick_move(flip_color(self.color))


def str_to_move(move: str) -> Move:
    move_dir = None
    for direction in dirs:
        if direction in move:
            move_dir = direction
            move = move.split(direction)
            break

    if move_dir is None:
        stone, c, r = move.zfill(3)
        return Move(stone=FLAT if stone == '0' else stone, col=c, row=r)
    else:
        ns = move[1]
        t = move[0]
        if t[0] not in cols:
            total = int(t[0])
            t = t[1:]
        else:
            total = 1
        c, r = t
        return Move(total=total, col=c, row=r, direction=move_dir, moves=list(map(int, ns)))


def load_moves_from_file(filename, out=False):
    with open(filename) as file:
        ptn = file.read()
        _, s = ptn.split("Size")
        ptn = s.split("\n")
        size = int(s[2])
        b = Board(size, size)
        curr_player = WHITE
        for iturn, turn in enumerate(ptn[2:]):
            if 'R' in turn:
                break
            for imove, move in enumerate(turn.split(" ")[1:]):  # Exclude the round number
                if move:
                    if iturn == 0:
                        curr_player = [BLACK, WHITE][imove]
                    elif iturn == 1 and imove == 0:
                        curr_player = WHITE

                    b.force(b.parse_move(str_to_move(move), curr_player))

                    if out:
                        print(move)
                        print(str_to_move(move))
                        print(b)
                        print("Road?:", b.road())

                    if curr_player == BLACK:
                        curr_player = WHITE
                    else:
                        curr_player = BLACK

                    yield b, move
    return b
