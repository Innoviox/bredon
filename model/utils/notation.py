from .constants import *
from dataclasses   import dataclass, field
from itertools     import starmap

@dataclass
class Move:
    total: int = 1
    stone: str = FLAT
    col: str = None
    row: int = None
    moves: list = field(default_factory=list)
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

    def __getitem__(self, turn):
        return self.moves[turn]

    def __repr__(self):
        return "PTN(%r)" % self.moves

    def __str__(self):
        return "\n".join(starmap(lambda i, moves: str(i) + ". " + " ".join(map(str, moves)),
                                 enumerate(self.moves, start=1)))

    def clear(self):
        self.moves.clear()