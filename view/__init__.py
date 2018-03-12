from model import *
import tkinter as tk

TILE_SIZE = 40
SQUARE_SIZE = 75




class ViewSquare(tk.Canvas):
    OFFSET = 3

    def __init__(self, master, i, j):
        #raised, sunken, groove, ridge
        #bd -> 5?
        tk.Canvas.__init__(self, master, width=SQUARE_SIZE, height=SQUARE_SIZE, bd=1, relief="sunken")
        self.pack()
        self.master = master
        self.i, self.j = i, j

    def _render(self, tile, idx):
        n = TILE_SIZE / 2
        s = SQUARE_SIZE / 2
        o = ViewSquare.OFFSET * idx
        d = 5
        x1, y1 = s - n, s - n - o + d
        x2, y2 = s + n, s + n - o + d
        if tile.stone == FLAT:
            self.create_rectangle(x1, y1, x2, y2, fill=tile.color)
        elif tile.stone == STAND:
            self.create_polygon(x1 + n * 1.5, y1,
                                x2, y1 + n * 0.5,
                                x1 + n * 0.5, y2,
                                x1, y1 + n * 1.5, fill=tile.color, outline='black')
        else:

            self.create_circle((x1+x2) / 2, (y1 + y2) / 2, s / 2, fill=tile.color)

    def render(self):
        self.delete("all")
        # self.create_rectangle(5, 5, SQUARE_SIZE, SQUARE_SIZE)
        for idx, tile in enumerate(self.master.board.board[self.i][self.j].tiles, start=1):
            self._render(tile, idx)

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def create_circle_arc(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)

class ViewBoard(tk.Frame):
    def __init__(self, master, board: Board):
        self.board = board
        self.size = board.size
        self.squares = []

        tk.Frame.__init__(self, master, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.pack(side=tk.LEFT, expand=1)
        self._init_gui()

    def _init_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                self.squares.append(ViewSquare(self, i, j))
                # self.squares[-1].grid(row=i, column=j)
                self.squares[-1].place_configure(x=i*SQUARE_SIZE + 1, y=j*SQUARE_SIZE + 1)

    def render(self):
        for s in self.squares:
            s.render()
