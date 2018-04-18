import random

from .utils import *

inf = float('inf')

class BaseAI(Player):
    def pick_move(self, input_fn=input):
        raise NotImplementedError()


class RandomAI(BaseAI):
    def pick_move(self, input_fn=input):
        return random.choice(list(self.board.generate_valid_moves(self)))

class MinimaxAI(BaseAI):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth

    def pick_opposing_move(self, input_fn=input):
        if self.board.valid_str("a1", flip_color(self.color)):
            return str_to_move("a1"), flip_color(self.color)
        return str_to_move(ascii_lowercase[self.board.size - 1] + str(self.board.size)), flip_color(self.color)

    def pick_move(self, input_fn=None, out=False):
        moves = self.board.generate_valid_moves(self.color, self.caps)
        best_eval = inf
        if self.depth % 2 == 1:
            best_eval *= -1
        best_move = None
        old_state = self.board.copy_board()
        alpha = -inf
        for move in moves:
            self.board.execute(move, self.color)
            alpha = self.minimax(self.depth - 1, self.board, -inf, inf, True, flip_color(self.color), self.board.copy_board()) * 4
            ev = self.board.evaluate(self.color)
            alpha -= ev / 2
            if abs(alpha) > THRESHOLD:
                alpha *= -1
            self.board.set(old_state)
            if (self.depth % 2 == 1 and alpha >= best_eval) or (self.depth % 2 == 0 and alpha <= best_eval):
                best_eval = alpha
                best_move = move
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color, old_state, out=False):
        if (board.road() or board.flat_win()):
            if maximising:
                return -MAX_N * depth
            else:
                return MAX_N  * depth
        elif depth == 0:
            return board.evaluate(color)
        
        moves = board.generate_valid_moves(color, self.caps)
        if maximising:
            b_eval = -inf
            for move in moves:
                board.execute(move, color)
                b_eval = max(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board(), out=out))
                board.set(old_state)
                alpha = max(alpha, b_eval)
                if beta <= alpha:
                    if beta < -THRESHOLD:
                        return beta
                    return -beta
        else:
            b_eval = inf
            for move in moves:
                board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board(), out=out))
                board.set(old_state)
                beta = min(beta, b_eval)
                if beta <= alpha:
                    if beta < -THRESHOLD:
                        return beta
                    return -beta
        return b_eval
