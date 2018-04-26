from .utils import *

from itertools import starmap


class PTN:
    def __init__(self, turn=1):
        self.moves = []
        self.turn = turn

    def append(self, move):
        if (not self.moves) or len(self.moves[-1]) == 2:
            self.moves.append([move])
        else:
            self.moves[-1].append(move)

    def get(self, turn, color: Colors):
        return self[turn][color.value]

    def clear(self):
        self.moves.clear()

    def __getitem__(self, turn):
        return self.moves[turn]

    def __repr__(self):
        return "PTN(%r)" % self.moves

    def __str__(self):
        return "\n".join(starmap(lambda i, moves: str(i) + ". " + " ".join(map(str, moves)),
                                 enumerate(self.moves, start=self.turn)))

    def __iter__(self):
        if self.moves:
            return iter(*self.moves)
        return iter([])


def parse_tps(tps):
    rows = [i.split(",") for i in tps.strip('[TPS"] ').split("/")]
    last, move, turn = rows[-1][-1].split()
    rows[-1][-1] = last
    for y, row in enumerate(rows):
        r = []
        for x, c in enumerate(row):
            if 'x' == c:
                r.append(Square(x, y))
            elif 'x' in c:
                r.extend([Square(x, y) for _ in range(int(c[1]))])
            else:
                tiles = []
                for stone in c[:-1]:
                    tiles.append(Tile(Colors(int(stone)-1), x=x, y=y))
                if c[-1] in STONES:
                    tiles[-1].stone = c[-1]
                else:
                    tiles.append(Tile(Colors(int(c[-1])-1), x=x, y=y))
                r.append(Square(x, y, tiles=tiles))
        rows[y] = r[:]
    board = list(zip(*reversed(rows)))
    for x, row in enumerate(board):
        for y, sq in enumerate(row):
            for tile in sq.tiles:
                sq.fix(tile=tile, x=y, y=x)
    return Board(len(rows[0]), board=board), move, turn
