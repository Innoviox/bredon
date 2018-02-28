import random


from .utils import Player, coords_to_tile, EMPTY, dirs, BLACK, WHITE, np, flip_color

class StaticAI(Player):
    def valid(self, move):
        return self.board.valid(self.board.parse_move(move, self.color))

    def generate_valid_moves(self, color):
        return filter(self.valid, self.generate_all_moves(color))

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
        # print("Picking move for ai color:", self.color)
        # print("Initial board state:")
        # print(self.board)
        moves = self.generate_valid_moves(self.color)
        best_eval = np.inf
        # if self.color == "B": best_eval *= -1
        best_move = None
        for move in moves:
            # print("Trying", move)
            new_board = self.board.execute(move, self.color)
            result = self.minimax(self.depth - 1, new_board, -np.inf, np.inf, True, flip_color(self.color))
            # if self.color in "WB": result *= -1
            # print("New board after move:")
            # print(new_board)
            # print("Evaluation:", result, new_board.evaluate(self.color, out=True))
            # if (self.color == "W" and result >= best_eval) or \
            #    (self.color == "B" and result <= best_eval):
            if result <= best_eval:
                # print("Setting best")
                best_eval = result
                best_move = move
            # print(move)
            # print(new_board)
            # input()
        # input()
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color):

        # print("Maximising" if maximising else "Minimising", end='')
        # print(" on", depth, maximising, color)
        # print(board)
        # print(board.road())
        # print(board.evaluate(color))

        if depth == 0:
            # print("\t", "returning")
            return board.evaluate(color)
        moves = self.generate_valid_moves(color)
        b_eval = None
        if maximising:
            b_eval = -np.inf
            for move in moves:
                # print("\t1a ", b_eval, alpha, beta)
                new_board = board.execute(move, color)
                b_eval = max(b_eval, self.minimax(depth - 1, new_board, alpha, beta, not maximising, flip_color(color)))
                alpha = max(alpha, b_eval)
                # print("\t1b ", b_eval, alpha, beta)
                if beta <= alpha:
                    # print("\t\tbreaking")
                    break
        else:
            b_eval = np.inf
            for move in moves:
                # print("\t2a ", b_eval, alpha, beta)
                new_board = board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, new_board, alpha, beta, not maximising, flip_color(color)))
                beta = min(beta, b_eval)
                # print("\t2b ", b_eval, alpha, beta)
                if beta <= alpha:
                    # print("\t\tbreaking")
                    break
        return b_eval
