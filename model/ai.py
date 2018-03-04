import random
from .utils import *

class StaticAI(Player):
    def pick_move(self):
        raise NotImplementedError()


class RandomAI(StaticAI):
    def pick_move(self):
        return random.choice(list(self.board.generate_valid_moves(self)))

class MinimaxAI(StaticAI):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth

    def pick_move(self, out=False):
        # print("Picking move for ai color:", self.color)
        # print("Initial board state:")
        # print(self.board)
        moves = self.board.generate_valid_moves(self.color, self.caps)
        best_eval = np.inf
        if self.depth % 2 == 1:
            best_eval *= -1
        # if self.color == "B": best_eval *= -1
        best_move = None
        old_state = self.board.copy_board()
        alpha = -np.inf
        for move in moves:
            # if move.stone == STAND:
            #     continue
            if out: print("Trying", move)
            self.board.execute(move, self.color)
            # print(self.board)
            alpha = self.minimax(self.depth - 1, self.board, -np.inf, np.inf, True, flip_color(self.color), self.board.copy_board()) * 4
            ev = self.board.evaluate(self.color)
            alpha -= ev / 2
            if abs(alpha) > 10000:
                alpha *= -1
            # s_alpha = -np.inf
            # if abs(alpha) > 10000:
            #     self.board.set(old_state)
            #     self.board.execute(str_to_move(STAND + move.get_square()), self.color)
            #     s_alpha =  -self.minimax(self.depth - 1, self.board, -np.inf, np.inf, True, flip_color(self.color), self.board.copy_board()) * 3
            #     s_alpha -= self.board.evaluate(self.color)

            # print("New board after move:")
            # print(self.board)
            if out: print("Evaluation:", alpha, ev, best_eval)# , out=True))
            self.board.set(old_state)
            # if self.color in "WB": result *= -1
            # if (self.color == "W" and result >= best_eval) or \
            #    (self.color == "B" and result <= best_eval):
            if (self.depth % 2 == 1 and alpha >= best_eval) or (self.depth % 2 == 0 and alpha <= best_eval):
                if out: print("Setting best")
                best_eval = alpha
                best_move = move
            # if s_alpha > alpha:
            #     best_eval = s_alpha
            #     best_move = STAND + move.get_square()
            # print(move)
            # print(new_board)
            # if out: input()
        # input()
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color, old_state, out=False):
        if out: print("\t" * (self.depth - depth) + "(minimax)", alpha, beta)
        if (board.road() or board.flat_win()):
            #depth >= self.depth - 2
            if maximising:
                if out: print("\t" * (self.depth - depth) + "\t(max) road breaking")
                return -1234567890
            else:
                if out: print("\t" * (self.depth - depth) + "\t(min) road breaking")
                return 1234567890
        elif depth == 0:
            if out: print("\t" * self.depth + "(0) ret", board.evaluate(color))
            return board.evaluate(color)


        moves = board.generate_valid_moves(color, self.caps)
        if maximising:
            b_eval = -np.inf
            for move in moves:
                if out: print("\t" * (self.depth - depth) + "(max) Trying", move, b_eval)
                board.execute(move, color)
                b_eval = max(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board(), out=out))
                board.set(old_state)
                alpha = max(alpha, b_eval)
                if beta <= alpha:
                    pass
                    if out: print("\t" * (self.depth - depth) + "\t(max) breaking", alpha, beta)
                    # if abs(beta) > 10000:
                    if beta < -10000:
                        return beta
                    return -beta # break
                    # return b_eval
        else:
            b_eval = np.inf
            for move in moves:
                if out: print("\t" * (self.depth - depth) + "(min) Trying", move, b_eval)
                board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board(), out=out))
                board.set(old_state)
                beta = min(beta, b_eval)
                if beta <= alpha:
                    pass
                    if out: print("\t" * (self.depth - depth) + "\t(min) breaking", alpha, beta)
                    if beta < -10000:
                        return beta
                    return -beta # break
                    # return b_eval
        return b_eval