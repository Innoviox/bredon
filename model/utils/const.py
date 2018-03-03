import collections as ct
import itertools as it

from string import ascii_lowercase as cols
from operator import sub


COLORS = "BW"
BLACK, WHITE = COLORS
COLORS_REV = ''.join(reversed(COLORS))
EMPTY = ' '
MARKS = '?!'

dirs = '+-<>'
UP, DOWN, LEFT, RIGHT = dirs
stones = 'FCS'
FLAT, CAP, STAND = stones
SIZE = 0

PseudoBoard = ct.namedtuple("PseudoBoard", ("w", "h", "board", "bool", "err", "type"))

sizes = {
    3: [10, 0],
    4: [15, 0],
    5: [21, 1],
    6: [30, 1],
    7: [40, 2],
    8: [50, 2]
}


def sums(n):
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in it.combinations(mid, i))
    return (list(map(sub, it.chain(s, e), it.chain(b, s))) for s in splits)


def tile_to_coords(t: str):
    return int(t[1]) - 1, cols.index(t[0])


def coords_to_tile(x: int, y: int):
    return cols[y] + str(x + 1)


def _next(obj, direction, size=None):
    if hasattr(obj, 'x') and hasattr(obj, 'y'):
        if direction == LEFT and obj.y > 0:
            return obj.x, obj.y - 1
        if direction == RIGHT and obj.y < SIZE - 1:
            return obj.x, obj.y + 1
        if direction == DOWN and obj.x > 0:
            return obj.x - 1, obj.y
        if direction == UP and obj.x < SIZE - 1:
            return obj.x + 1, obj.y
        raise ValueError("Out of bounds")
    raise TypeError("Object must have an x and y attribute")

def flip_color(color):
    return COLORS_REV[COLORS.index(color)]
