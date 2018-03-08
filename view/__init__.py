from model import *
import tkinter as tk

TILE_SIZE = 40
SQUARE_SIZE = 75

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc



class ViewSquare(tk.Canvas):
    OFFSET = 10

    def __init__(self, master, i, j):
        tk.Canvas.__init__(self, master, width=SQUARE_SIZE, height=SQUARE_SIZE)
        self.grid(row=j + 1, column=i + 1)
        print(self.grid_info())
        self.pack()
        self.master = master
        self.i, self.j = i, j

    def _render(self, tile, idx):
        n = ViewSquare.OFFSET * idx
        self.create_rectangle(TILE_SIZE + n, TILE_SIZE + n, n, n, fill=tile.color)

    def render(self):
        self.delete("all")
        self.create_rectangle(5, 5, SQUARE_SIZE, SQUARE_SIZE, width=5)
        for idx, tile in enumerate(self.master.board.board[self.i][self.j].tiles, start=1):
            self._render(tile, idx)


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
                self.squares[-1].grid(row=i, column=j)

    def render(self):
        for s in self.squares:
            s.render()
