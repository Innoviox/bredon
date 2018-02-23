import random
import itertools as it
from operator import sub

from .utils import Player, coords_to_tile, EMPTY, dirs, BLACK, WHITE

def sums(n):
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in it.combinations(mid, i))
    return (list(map(sub, it.chain(s, e), it.chain(b, s))) for s in splits)

class StaticAI(Player):
    def generate_all_moves(self):
        for y in range(self.board.h):
            for x in range(self.board.w):
                s = coords_to_tile(x, y)
                tile = self.board.get(x, y)
                if tile == EMPTY:
                    yield s
                    for stone in 'CS':
                        yield stone + s
                else:
                    if tile.tiles[0].color == self.color:
                        for direction in dirs:
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
        return self.board.valid(self.board.parse_move(move, self.color))

    def generate_valid_moves(self):
        return filter(self.valid, self.generate_all_moves())

    def other_color(self):
        return [BLACK, WHITE][self.color == BLACK]

    def pick_move(self):
        raise NotImplementedError()


class RandomAI(StaticAI):
    def pick_move(self):
        return random.choice(list(self.generate_valid_moves()))


class LookAhead1AI(StaticAI):
    def __init__(self, board, color):
        super().__init__(board, color)
        self.ai = StaticAI(board, self.other_color())

    def pick_move(self):
        moves = self.generate_valid_moves()

        lost = []
        wins = []
        cont = []
        checked = []
        for move in moves:
            board_after = self.board.copy()
            board_after.force_str(move, self.color)
            l = False
            if board_after.winner([self, self.ai]) == self:
                wins.append(move)
                break
            else:
                self.ai.board = board_after
                for ai_move in self.ai.generate_valid_moves():
                    if ai_move not in checked:
                        board_after_ai = self.ai.board.copy()
                        board_after_ai.force_str(ai_move, self.ai.color)
                        if board_after_ai.winner([self, self.ai]) == self.ai.color:
                            lost.append(move)
                            l = True
                            break
                    checked.append(ai_move)
            if not l:
                cont.append(move)

        print("Wins:", wins)
        print("Cont:", cont)
        print("Lost:", lost)

        if wins:
            return random.choice(wins)
        elif cont:
            return self.choose(cont)
        else:
            print("I lose!")
            return random.choice(lost)

    def choose(self, moves):
        # TODO: Implement heuristic
        return random.choice(moves)


class AI(StaticAI):
    def pick_move(self):
        if not self.will_lose():
            self.build()
        else:
            self.block()

    def will_lose(self):
        opponent = StaticAI(self.board, self.other_color())
        for m in opponent.generate_valid_moves():
            board_after = opponent.board.copy()
            board_after.force_str(m, opponent.color)
            if board_after.winner([self, opponent]) == opponent.color:
                return True
        return False

    def build(self):
        pass

    def block(self):
        pass