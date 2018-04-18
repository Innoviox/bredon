from view import *  # imports model
import time


class Game():
    def __init__(self, size=5, board=None, white_type=HUMAN, black_type=AI(3)):
        self.board = Board(size) if board is None else board
        self.player_1: Player = self._init_player(WHITE, white_type)
        self.player_2: Player = self._init_player(BLACK, black_type)
        self.players = [self.player_1, self.player_2]

        self.stones = {i: FLAT for i in COLORS}

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
        if turn <= 1:
            m, c = player.pick_opposing_move(input_fn=input_fn)
            self.stones[c] = STONES
        else:
            m = player.pick_move(input_fn=input_fn)
            c = player.color
            if CAP in str(m):
                self.stones[c] = FLAT + STAND
        print(time.time() - t)
        player._do(m, c)
        return str(m) + " "

    def run(self):
        ptn = ""
        turn = 1
        while True:
            ptn += str(turn) + ". "
            for player in self.players:
                ptn += self._run(player, turn)
                w = self.board.winner(self.players, t=True)
                print(ptn)
                if w:
                    print(w, "won!")
                    return
            ptn += "\n"
            turn += 1

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

        self.flats.grid(row=0, column=0)
        self.vboard.grid(row=2, column=0)
        self.tiles.grid(row=2, column=6, rowspan=self.board.size)

        self.turn = 0
        self.ptn = ""
        self.running = False
        self.player = 0
        self.first = True
        self.event = None

        self.viz()

    def exec(self, *event, ai=False):
        if not ai and not self.vboard.input.get():
            return
        if not self.running:
            return
        elif self.player == 0:
            self.ptn += "\n%d. " % (self.turn + 1)
            self.turn += 1

        p = self.players[self.player]
        move = self._run(p, self.turn, input_fn=lambda _: self.vboard.input.get())
        self.ptn += move
        print(self.ptn)
        self.viz()
        self.vboard.input.delete(0, "end")
        self.vboard.i = 0
        if self.vboard.grabbed:
            self.vboard.clear(r=False)
        self.vboard.board = self.board
        self.viz()
        self.player = (self.player + 1) % 2
        if isinstance(self.players[self.player], BaseAI):
            self.exec(ai=True)

        w = self.board.winner(self.players, t=True)
        if w:
            print(w, "won!")

    def viz(self):
        self.flats.render()
        self.tiles.render()
        self.vboard.render(flip_color(self.players[self.player].color))
        self.update_idletasks()
        self.update()

    def mainloop(self, n=0):
        self.running = True
        if isinstance(self.players[self.player], BaseAI):
            self.exec(ai=True)
        super(tk.Tk, self).mainloop(n=n)

    def get_color(self):
        return self.players[self.player].color
