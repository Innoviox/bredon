from view import *  # imports model
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

    def _run(self, player, turn, input_fn=input):
        # self.viz()
        t = time.time()
        if turn == 1:
            m, c = player.pick_opposing_move(input_fn=input_fn)
            print(m, c)
        else:
            m = player.pick_move(input_fn=input_fn)
            c = player.color
        print(time.time() - t)
        player._do(m, c)
        return str(m) + " "


class TextGame(Game):
    def viz(self):
        print(self.board)


class ViewGame(tk.Tk, Game):
    def __init__(self, **kw):
        tk.Tk.__init__(self)
        Game.__init__(self, **kw)
        self.wm_title("tak")
        self.vboard = ViewBoard(self)
        self.tiles = TilesCanvas(self)
        self.flats = FlatCanvas(self)

        self.flats.grid(row=0, column=0)  #, columnspan=self.board.size)
        self.vboard.grid(row=2, column=0)
        self.tiles.grid(row=2, column=6, rowspan=self.board.size)
        self.viz()

        self.turn = 1
        self.ptn = ""
        self.running = False
        self.player = 0
        self.first = True
        self.event = None

    def exec(self, *event, ai=False):
        if not ai and not self.vboard.input.get():
            return
        if not self.running:
            return
        # elif self.first:
        #     self.ptn = "1. "
        #     self.first = False
        elif self.player == 0:
            self.ptn += "\n%d. " % self.turn
            self.turn += 1

        old_board = self.board.copy()

        p = self.players[self.player]
        move = self._run(p, self.turn, input_fn=lambda _: self.vboard.input.get())
        self.ptn += move
        print(self.ptn)

        self.vboard.input.delete(0, "end")
        self.vboard.i = 0
        self.vboard.execute(move.strip(), p, old_board)
        self.viz()
        self.player = (self.player + 1) % 2
        if isinstance(self.players[self.player], StaticAI):
            self.exec(ai=True)

        w = self.board.winner(self.players, t=True)
        if w:
            print(w, "won!")

    def viz(self):
        self.flats.render()
        self.tiles.render()
        print("rendering!")
        self.vboard.render()
        self.update_idletasks()
        self.update()

    def run(self):
        self.running = True
        if isinstance(self.players[self.player], StaticAI):
            self.exec(ai=True)
        self.mainloop()

    # def run(self):
    #     ptn = ""
    #     turn = 1
    #     while True:
    #         ptn += str(turn) + ". "
    #         for player in self.players:
    #             old_board = self.board.copy()
    #             move = self._run(player, turn, input_fn=self.vboard.input.get)
    #             self.vboard.execute(move.strip(), player.color, old_board)
    #             ptn += move
    #             w = self.board.winner(self.players, t=True)
    #             print(ptn)
    #             if w:
    #                 print(w, "won!")
    #                 return
    #         ptn += "\n"
    #         turn += 1
