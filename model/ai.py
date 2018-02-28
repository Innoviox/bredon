import random


from .utils import Player, coords_to_tile, EMPTY, dirs, BLACK, WHITE, np, flip_color

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

    def pick_move(self):
        # print("Picking move for ai color:", self.color)
        # print("Initial board state:")
        # print(self.board)
        moves = self.board.generate_valid_moves(self.color, self.caps)
        best_eval = -np.inf
        # if self.color == "B": best_eval *= -1
        best_move = None
        old_state = self.board.copy_board()
        alpha = np.inf
        for move in moves:
            print("Trying", move)
            self.board.execute(move, self.color)
            alpha = -self.minimax(self.depth - 1, self.board, -np.inf, np.inf, True, flip_color(self.color), self.board.copy_board()) * 3
            ev = self.board.evaluate(self.color)
            alpha -= ev
            # print("New board after move:")
            # print(self.board)
            print("Evaluation:", alpha, ev)# , out=True))
            self.board.set(old_state)
            # if self.color in "WB": result *= -1
            # if (self.color == "W" and result >= best_eval) or \
            #    (self.color == "B" and result <= best_eval):
            if alpha >= best_eval:
                # print("Setting best")
                best_eval = alpha
                best_move = move
            # print(move)
            # print(new_board)
            # input()
        # input()
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color, old_state):

        # print("Maximising" if maximising else "Minimising", end='')
        # print(" on", depth, maximising, color)
        # print(board)
        # print(board.road())
        # print(board.evaluate(color))

        if board.road():

            # print(board)
            if maximising:
                return -1234567890
            else:
                return 1234567890
        elif depth == 0: # or board.road():
            # print("\t", "returning")
            return board.evaluate(color)

        moves = board.generate_valid_moves(color, self.caps)
        if maximising:
            b_eval = -np.inf
            for move in moves:
                # print("\t" * (self.depth - depth) + "(max) Trying", move)

                # print("\t1a ", b_eval, alpha, beta)
                board.execute(move, color)
                # print(board, board.road(), board.road(out = True))
                # if str(move) == "c1": input()
                b_eval = max(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board()))
                board.set(old_state)
                alpha = max(alpha, b_eval)
                # print("\t1b ", b_eval, alpha, beta)
                if beta <= alpha:
                    pass
                    # print("\t" * (self.depth - depth) + "\t(max) breaking", alpha, beta)
                    break
        else:
            b_eval = np.inf
            for move in moves:
                # print("\t2a ", b_eval, alpha, beta)
                # print("\t" * (self.depth - depth) + "(min) Trying", move)
                board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, flip_color(color), board.copy_board()))
                board.set(old_state)
                beta = min(beta, b_eval)
                # print("\t2b ", b_eval, alpha, beta)
                if beta <= alpha:
                    pass
                    # print("\t" * (self.depth - depth) + "\t(min) breaking", alpha, beta)
                    break
        return b_eval
