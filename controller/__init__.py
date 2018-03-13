from model import *
from view import *
import time

HUMAN = "human", None
AI = "ai"

class Game():
    def __init__(self, size=5, board=None, white_type=HUMAN, black_type=(AI, 3)):
        self.board = Board(size) if board is None else board
        self.player_1: Player = self._init_player(WHITE, white_type)
        self.player_2: Player = self._init_player(BLACK, black_type)
        self.players = [self.player_1, self.player_2]

    def _init_player(self, color, types) -> Player:
        name, depth = types
        if name == HUMAN[0]:
            return Player(self.board, color)
        else:
            return MinimaxAI(self.board, color, depth)

    def viz(self):
        raise NotImplementedError()

    def _run(self, player, turn):
        self.viz()
        t = time.time()
        if turn == 1:
            m, c = player.pick_opposing_move()
        else:
            m = player.pick_move()
            c = player.color
        print(time.time() - t)
        player._do(m, c)
        return str(m) + " "

class TextGame(Game):
    def viz(self):
        print(self.board)



class ViewGame(tk.Tk, Game):
    def __init__(self, **kw):
        tk.Tk.__init__(self, "tak")
        Game.__init__(self, **kw)
        self.vboard = ViewBoard(self, self.board)
        self.update()

    def viz(self):
        # self.vboard.render()
        self.update_idletasks()
        self.update()

    def run(self):
        ptn = ""
        turn = 1
        while True:
            ptn += str(turn) + ". "
            for player in self.players:
                old_board = self.board.copy()
                move = self._run(player, turn)
                self.vboard.execute(move.strip(), player.color, old_board)
                ptn += move
                w = self.board.winner(self.players, t=True)
                print(ptn)
                if w:
                    print(w, "won!")
                    return
            ptn += "\n"
            turn += 1
