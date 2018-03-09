import collections as ct
import itertools as it
import numpy as np
import dataclasses as dc
import tabulate as tb
import functools as fc

from string import ascii_lowercase as cols
from operator import sub


COLORS = ("black", "white")
BLACK, WHITE = COLORS
COLORS_REV = tuple(reversed(COLORS))
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

class Next:
    __slots__ = 'x', 'y'
    def next(obj, direction, size):
        if direction == LEFT and obj.y > 0:
            return obj.x, obj.y - 1
        if direction == RIGHT and obj.y < size - 1:
            return obj.x, obj.y + 1
        if direction == DOWN and obj.x > 0:
            return obj.x - 1, obj.y
        if direction == UP and obj.x < size - 1:
            return obj.x + 1, obj.y
        return obj.x, obj.y

def flip_color(color):
    return COLORS_REV[COLORS.index(color)]