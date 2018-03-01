from model import *

HUMAN = "human"
AI = "ai"

class Game:
    def __init__(self, size=5, board=None, white_type=(HUMAN, None), black_type=(AI, 3)):
        self.board = Board(w=size, h=size) if board is None else board
        self.player_1: Player = self._init_player(WHITE, white_type)
        self.player_2: Player = self._init_player(BLACK, black_type)
        self.players = [self.player_1, self.player_2]

    def _init_player(self, color, types) -> Player:
        name, depth = types
        if name == HUMAN:
            return Player(self.board, color)
        else:
            return MinimaxAI(self.board, color, depth)

    def run(self):
        ptn = ""
        turn = 1
        while True:
            ptn += str(turn) + ". "
            for player in self.players:
                print(self.board)
                if turn == 1:
                    m = player.pick_opposing_move()
                else:
                    m = player.pick_move()
                ptn += str(m) + " "
                player.do(m)
                w = self.board.winner(self.players)
                print(ptn)
                if w:
                    print(w, "won!")
                    return
            ptn += "\n"
            turn += 1

