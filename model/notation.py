from .utils import *

from itertools import starmap


class PTN:
    def __init__(self):
        self.moves = []

    def append(self, move):
        if (not self.moves) or len(self.moves[-1]) == 2:
            self.moves.append([move])
        else:
            self.moves[-1].append(move)

    def get(self, turn, color):
        return self[turn][COLORS.index(color)]

    def clear(self):
        self.moves.clear()

    def __getitem__(self, turn):
        return self.moves[turn]

    def __repr__(self):
        return "PTN(%r)" % self.moves

    def __str__(self):
        return "\n".join(starmap(lambda i, moves: str(i) + ". " + " ".join(map(str, moves)),
                                 enumerate(self.moves, start=1)))

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
                    tiles.append(Tile(COLORS[int(stone)-1], x=x, y=y))
                if c[-1] in STONES:
                    tiles[-1].stone = c[-1]
                else:
                    tiles.append(Tile(COLORS[int(c[-1])-1], x=x, y=y))
                r.append(Square(x, y, tiles=tiles))
        rows[y] = r

    return Board(len(rows[0]), board=zip(*reversed(rows)))