import random


from .utils import Player, coords_to_tile, EMPTY, dirs, BLACK, WHITE, np, flip_color
infinity = float('inf')

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    return argmin(seq, lambda x: -fn(x))


class StaticAI(Player):
    def other_color(self):
        return [BLACK, WHITE][self.color == BLACK]

    def pick_move(self):
        raise NotImplementedError()


class RandomAI(StaticAI):
    def pick_move(self):
        return random.choice(list(self.generate_valid_moves()))

class MinimaxAI(StaticAI):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth

    def minimax_root(self, maximising):
        moves = self.board.generate_valid_moves(self.color, self.caps)
        best_move = -np.inf
        best_move_found = None
        alpha = -np.inf
        for move in moves:
            # print("Trying move", move)
            new_board = self.board.execute(move, self.color)
            # print(new_board)
            alpha = self.minimax(self.depth - 1, new_board, alpha, 10000, not maximising, flip_color(self.color))
            # print(new_board.evaluate(self.color), alpha)
            if alpha >= best_move:
                best_move = alpha
                best_move_found = move
            # put()
        return best_move_found

    def minimax(self, depth, board, alpha, beta, maximising, color):
        # print(depth, alpha, beta, maximising, color)
        # print(board)
        if depth == 0:
            # print("\t0 returning", -board.evaluate(color))
            return -board.evaluate(color)
        moves = board.generate_valid_moves(color, self.caps)
        if maximising:
            # print("Maximising!")
            best_move = -np.inf
            for move in moves:
                new_board = board.execute(move, self.color)
                best_move = max(best_move, self.minimax(depth - 1, new_board, alpha, beta, not maximising, flip_color(self.color)))
                alpha = max(alpha, best_move)
                # if best_move == 14:
                    # print("\t\ta", move)
                    # print(new_board)
                if beta <= alpha:
                    # print("\t1 returning", move, best_move)
                    return best_move
        else:
            # print("Minimising!")
            best_move = np.inf
            for move in moves:
                new_board = board.execute(move, self.color)
                best_move = min(best_move, self.minimax(depth - 1, new_board, alpha, beta, not maximising, flip_color(self.color)))
                # if best_move == 14: print("\t\ta", move)
                beta = min(beta, best_move)
                if beta <= alpha:
                    # print("\t2 returning", move, best_move)
                    return best_move
        # print("\t3 returning", best_move)
        return best_move


    def pick_move(self):
        return self.minimax_root(True)