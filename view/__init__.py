from model import *
import tkinter as tk
import time

TILE_SIZE = 40
SQUARE_SIZE = 75
ANIM_STEPS = 30


class ViewSquare:
    def __init__(self, master, i, j, width=SQUARE_SIZE, height=SQUARE_SIZE):
        self.width = width
        self.height = height
        self.master = master
        self.i, self.j = i, j
        self.ix, self.jy = self.i * SQUARE_SIZE + 2, self.j * SQUARE_SIZE + 2
        self.tags = str(i) + "." + str(j)
        self.ids = []

    def _render(self, tile, idx, offset_x=0.0, offset_y=0.0):
        n, s, o, d = self._calc_nsod(idx)

        x1, y1 = offset_x + self.ix + s - n, offset_y + self.jy + s - n - o + d
        x2, y2 = offset_x + self.ix + s + n, offset_y + self.jy + s + n - o + d
        if tile.stone == FLAT:
            return self.master.canvas.create_rectangle(x1, y1, x2, y2, fill=tile.color, tags=(self.tags, idx))
        elif tile.stone == STAND:
            return self.master.canvas.create_polygon(x1 + n * 1.5, y1,
                                                     x2, y1 + n * 0.5,
                                                     x1 + n * 0.5, y2,
                                                     x1, y1 + n * 1.5, fill=tile.color, outline='black', tags=(self.tags, idx))
        else:
            return self.create_circle(*self.find_center(idx, offset_x, offset_y), s / 2, fill=tile.color, tags=(self.tags, idx))

    def find_center(self, idx, offset_x=0.0, offset_y=0.0):
        n, s, o, d = self._calc_nsod(idx)
        return offset_x + self.ix + s, offset_y + self.jy + s - o + d

    def _calc_nsod(self, idx):
        return TILE_SIZE / 2, SQUARE_SIZE / 2, 3 * idx, 5

    def render(self, active=False):
        self.master.canvas.create_rectangle(self.ix, self.jy, self.ix + SQUARE_SIZE, self.jy + SQUARE_SIZE,
                                            fill="green" if active else "white")
        self.ids = [self._render(tile, idx) for idx, tile in enumerate(self.get_tiles(self.master.board), start=1)]

    def create_circle(self, x, y, r, **kwargs):
        return self.master.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def get_tiles(self, board):
        return board.board[self.i][self.j].tiles

class ViewBoard(tk.Frame):
    def __init__(self, master, board: Board):
        self.board = board
        self.size = board.size
        self.squares = []

        tk.Frame.__init__(self, master, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.canvas = tk.Canvas(self, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.pack()
        self.canvas.pack()
        self._init_gui()
        self.actives = [False for _ in range(self.size ** 2)]

    def _init_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                self.squares.append(ViewSquare(self, i, j))

    def execute(self, move, player, old_board):
        new_board = self.board.copy()
        new_board.force_str(move, player)
        idx = 0
        for rn, ro in zip(new_board.board, old_board.board):
            for nsq, sq in zip(rn, ro):
                if str(nsq) != str(sq):
                    self.actives[idx] = True
                idx += 1
        self.render()
        if str_to_move(move).direction is not None:
            self.animate(move, old_board)

    def get_squares(self, m, old_board):
        s = old_board.board[int(m.row) - 1][int(cols.index(m.col))]
        d = m.direction
        if not m.moves:
            print("yielding1")
            yield (s.x, s.y), 1
        for n in m.moves:
            print("yielding", n)
            yield (s.x, s.y), n
            s = Square(*s.next(d, self.size))

    def animate(self, move, old_board):
        print("ANIMATING!")
        m = str_to_move(move)
        sqs, ns = [], []
        for s, n in self.get_squares(m, old_board):
            sqs.append(s)
            ns.append(n)
        print("Found", m, move, sqs, ns)
        for i, n in enumerate(ns):
            print("animating", i, n)
            moved, sqs = sqs[:n], sqs[n:]
            for idx, sq in enumerate(moved, start=1):
                print("\t_animating", sq)
                self._animate(sq, m.direction, i, idx, old_board)

    def _animate(self, sq, direction, i, idx, old_board):
        print("_animating", sq, direction, i, idx)
        vis = self.get_square(sq)
        nvis = Square(*sq).tru_next(direction, self.size)
        for j in range(i):
            nvis = Square(*nvis).tru_next(direction, self.size)
        # if vis.i == nvis[0] and vis.j == nvis[1]:
        #     if (vis.i, vis.j) in ((0, 1), (1, 0)):
        #         nvis = (0, 0)
        nvis = self.get_square(nvis)
        print(vis.i, vis.j, nvis.i, nvis.j)
        ts = vis.get_tiles(old_board)
        nts = nvis.get_tiles(old_board)
        old_y, old_x = vis.find_center(0)
        new_y, new_x = nvis.find_center(0)
        if direction in LEFT + RIGHT:
            # new_x = old_x
            new_y -= (len(nts) - 1 + idx) * 3
        else:
            # new_y = old_y
            new_x -= (len(nts) - 1 + idx) * 3
        # new_x -= (len(ts) + idx) * 3
        tile = ts[i]
        xi, yi = (new_x - old_x) / ANIM_STEPS, (new_y - old_y) / ANIM_STEPS
        print(ts, len(ts), idx, old_x, old_y, new_x, new_y, xi, yi)
        _id = vis.ids[i]
        for k in range(ANIM_STEPS):
            self.canvas.delete(_id)
            _id = vis._render(tile, i, -(yi * k), (xi * k))
            self.update()

    def get_square(self, sq) -> ViewSquare:
        return self.squares[sq[0] * self.size + sq[1]]

    def render(self):
        self.canvas.delete("all")
        for s, a in zip(self.squares, self.actives):
            s.render(a)
        self.canvas.create_line(3, 3, self.winfo_width(), 3, tags="line")
        self.canvas.create_line(3, 3, 3, self.winfo_height(), tags="line")
        self.actives = [False for _ in range(self.size ** 2)]
