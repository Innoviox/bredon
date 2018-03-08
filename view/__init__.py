from model import *
import tkinter as tk

TILE_SIZE = 50

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
        tk.Canvas.__init__(self, master, width=TILE_SIZE, height=TILE_SIZE)
        self.grid(row=j + 1, column=i + 1)
        print(self.grid_info())
        self.pack()
        self.master = master
        self.i, self.j = i, j

    def _render(self, tile, idx):
        n = ViewSquare.OFFSET * idx
        print("\t\trendering tile", n, n, n + TILE_SIZE, n + TILE_SIZE, tile.color)
        self.create_rectangle(n, n, n + TILE_SIZE, n + TILE_SIZE, fill=tile.color)
        self.update()

    def render(self):
        self.delete("all")
        print("\trecv render square")
        self.create_rectangle(5, 5, TILE_SIZE, TILE_SIZE, width=5)
        for idx, tile in enumerate(self.master.board.board[self.i][self.j].tiles, start=1):
            self._render(tile, idx)


class ViewBoard(tk.Frame):
    def __init__(self, master, board: Board):
        self.board = board
        self.size = board.size
        self.squares = []

        tk.Frame.__init__(self, master, width=self.size * TILE_SIZE, height=self.size * TILE_SIZE)
        self.pack(side=tk.LEFT, expand=1)
        self._init_gui()

    def _init_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                self.squares.append(ViewSquare(self, i, j))
                self.squares[-1].grid(row=i, column=j)

    def render(self):
        for s in self.squares:
            print("\trendering square")
            s.render()
