import random


from .utils import Player, coords_to_tile, EMPTY, dirs, BLACK, WHITE, np

class StaticAI(Player):
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

class MinimaxAI(StaticAI):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth

    def pick_move(self):
        moves = self.generate_valid_moves()
        best_eval = -np.inf
        best_move = None
        for move in moves:
            new_board = self.board.execute(move, self.color)
            result = self.minimax(self.depth - 1, new_board, -np.inf, np.inf, True, self.color)
            if result >= best_eval:
                best_eval = result
                best_move = move
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color):
        # print("Minimaxing on", depth, maximising)
        # print(board)
        # print(board.evaluate(color))
        if depth == 0:
            # print("\t", "returning")
            return -board.evaluate(color)
        moves = self.generate_valid_moves()
        b_eval = None
        if maximising:
            b_eval = -np.inf
            for move in moves:
                new_board = board.execute(move, color)
                b_eval = max(b_eval, self.minimax(depth - 1, new_board, alpha, beta, not maximising, "WB"["BW".index(color)]))
                alpha = max(alpha, b_eval)
                if beta <= alpha:
                    break
        else:
            b_eval = np.inf
            for move in moves:
                new_board = board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, new_board, alpha, beta, not maximising, "WB"["BW".index(color)]))
                beta = min(beta, b_eval)
                if beta <= alpha:
                    break
        return b_eval
