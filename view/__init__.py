from model import *
import tkinter as tk

TILE_SIZE = 40
SQUARE_SIZE = 75




class ViewSquare:
    OFFSET = 3

    def __init__(self, master, i, j, width=SQUARE_SIZE, height=SQUARE_SIZE):
        self.width = width
        self.height = height
        self.master = master
        self.i, self.j = i, j
        self.ix, self.jy = (self.i) * SQUARE_SIZE + 2, (self.j) * SQUARE_SIZE + 2

    def _render(self, tile, idx):
        n = TILE_SIZE / 2
        s = SQUARE_SIZE / 2
        o = ViewSquare.OFFSET * idx
        d = 5
        x1, y1 = self.ix + s - n, self.jy + s - n - o + d
        x2, y2 = self.ix + s + n, self.jy + s + n - o + d
        if tile.stone == FLAT:
            self.master.canvas.create_rectangle(x1, y1, x2, y2, fill=tile.color)
        elif tile.stone == STAND:
            self.master.canvas.create_polygon(x1 + n * 1.5, y1,
                                              x2, y1 + n * 0.5,
                                              x1 + n * 0.5, y2,
                                              x1, y1 + n * 1.5, fill=tile.color, outline='black')
        else:

            self.create_circle((x1 + x2) / 2, (y1 + y2) / 2, s / 2, fill=tile.color)

    def render(self):
        self.master.canvas.create_rectangle(self.ix, self.jy, self.ix + SQUARE_SIZE, self.jy + SQUARE_SIZE)
        for idx, tile in enumerate(self.master.board.board[self.i][self.j].tiles, start=1):
            self._render(tile, idx)

    def create_circle(self, x, y, r, **kwargs):
        return self.master.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

class ViewBoard(tk.Frame):
    def __init__(self, master, board: Board):
        self.board = board
        self.size = board.size
        self.squares = []

        tk.Frame.__init__(self, master, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.canvas = tk.Canvas(self, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.pack(side=tk.LEFT, expand=1)
        self.canvas.pack()
        self._init_gui()

    def _init_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                self.squares.append(ViewSquare(self, i, j))
                # self.squares[-1].grid(row=i, column=j)
                # self.squares[-1].place_configure(x=i*SQUARE_SIZE + 1, y=j*SQUARE_SIZE + 1)

    def render(self):
        self.canvas.delete("all")
        self.canvas.create_line(3, 3, self.winfo_width(), 3)
        self.canvas.create_line(3, 3, 3, self.winfo_height())
        for s in self.squares:
            s.render()

