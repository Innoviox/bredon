import tkinter as tk
from typing import Optional

from model import *


tk.Canvas.create_circle = lambda self, x, y, r, **kwargs: self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


class ViewSquare:
    def __init__(self, master, i, j, width=SQUARE_SIZE, height=SQUARE_SIZE):
        self.width = width
        self.height = height
        self.master = master
        self.i, self.j = i, j
        self.ix, self.jy = self.i * SQUARE_SIZE + 2, self.j * SQUARE_SIZE + 2
        self.tags = str(i) + "." + str(j)
        self.ids = []
        self.nridx = None

    def render_tile(self, tile, idx, offset_x=0.0, offset_y=0.0):
        if tile is None: return
        o = OFFSET_STEP * idx

        x1, y1 = offset_x + self.ix + s - n, offset_y + self.jy + s - n - o + d
        x2, y2 = offset_x + self.ix + s + n, offset_y + self.jy + s + n - o + d
        if tile.stone == FLAT:
            return self.master.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill=tile.color)
        elif tile.stone == STAND:
            if tile.color == WHITE:
                points = (
                    x1 + n * 1.5, y1,
                    x2, y1 + n * 0.5,
                    x1 + n * 0.5, y2,
                    x1, y1 + n * 1.5
                )
            else:
                points = (
                    x1 + n * 0.5, y1,
                    x2, y1 + n * 1.5,
                    x1 + n * 1.5, y2,
                    x1, y1 + n * 0.5
                )

            return self.master.canvas.create_polygon(*points, fill=tile.color, outline='black',
                                                     tags=(self.tags, idx))
        else:
            return self.create_circle(*self.find_center(idx, offset_x, offset_y), s / 2, fill=tile.color,
                                      tags=(self.tags, idx))

    def find_center(self, idx, offset_x=0.0, offset_y=0.0):
        o = OFFSET_STEP * idx
        return offset_x + self.ix + s, offset_y + self.jy + s - o + d

    def render(self, active=False, possible=False):
        self.rect = self.master.canvas.create_rectangle(self.ix, self.jy, self.ix + SQUARE_SIZE, self.jy + SQUARE_SIZE,
                                                        fill="green" if active else "white")
        if possible:
            self.circle = self.create_circle(self.ix + s, self.jy + s, s - 5, outline="blue", width=5)
        self.ids = []
        tiles = self.get_tiles(self.master.board)[:]
        if self.nridx is not None:
            tiles.insert(self.nridx, None)
        self.ids = [self.render_tile(tile, idx) for idx, tile in enumerate(self.get_tiles(self.master.board), start=1)]

    def create_circle(self, x, y, r, **kwargs):
        return self.master.canvas.create_circle(x, y, r, **kwargs)

    def get_square(self, board):
        return board.board[self.i][self.j]

    def get_tiles(self, board):
        return self.get_square(board).tiles

    def s(self, b):
        return self.tags + " " + str(self.get_tiles(b))


class ViewBoard(tk.Frame):
    def __init__(self, master):
        self.board = master.board
        self.size = master.board.size
        self.squares = []

        tk.Frame.__init__(self, master, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        self.pack_propagate(0)
        self.canvas = tk.Canvas(self, width=self.size * SQUARE_SIZE, height=self.size * SQUARE_SIZE)
        # self.canvas.pack()
        self._init_gui()
        self.actives = [False for _ in range(self.size ** 2)]
        self.move = None

        # Saved states for movement
        self.i = 1
        self.grabbed: Optional[bool, ViewSquare] = False
        self.grabbed_first = False
        self.direction = False
        self.nridx = 0
        self.moves = []

        self.canvas.bind("<2>", self.master.exec)
        self.canvas.bind("<1>", self.click)

    def _init_gui(self):
        self.row_labels = [tk.Label(self, text=ascii_lowercase[i], width=SQUARE_SIZE // 20, height=1)  #, bd=5, relief=tk.GROOVE)
                           .grid(column=i + 1, row=0)
                           for i in range(self.size)]
        self.col_labels = [tk.Label(self, text=i + 1, height=SQUARE_SIZE // 20, width=1)  #, bd=5, relief=tk.GROOVE)
                           .grid(column=0, row=i + 1)
                           for i in range(self.size)]
        self.canvas.grid(row=1, column=1, columnspan=self.size, rowspan=self.size)

        self.input = tk.Entry(self)
        self.input.bind("<Return>", self.master.exec)

        self.exec_button = tk.Button(self, text="Execute", command=self.master.exec)

        self.clear_button = tk.Button(self, text="Clear", command=self.clear)

        self.input.grid(row=6, column=0, columnspan=self.size - 2)
        self.exec_button.grid(row=6, column=self.size - 2)
        self.clear_button.grid(row=6, column=self.size - 1)

        for i in range(self.size):
            for j in range(self.size):
                self.squares.append(ViewSquare(self, i, j))

    def click(self, event):
        def _run(s, f=False):
            self.input.delete(0, tk.END)
            self.input.insert(0, s)
            self.move = None
            self.render(flip_color(self.master.get_color()))
            self.b = self.board.copy()
            self.board = self.master.board.copy()
            self.board.force_str(self.input.get(), self.master.players[self.master.player].color)
            self.execute(self.input.get().strip(), self.master.players[self.master.player], self.b)
            self.render(flip_color(self.master.get_color()))
            self.move = None
            if not f: self.board = self.b

        stones = self.master.stones[self.master.get_color()]
        self.i = (self.i + 1) % len(stones)
        x, y = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
        sq = self.squares[x * self.size + y]
        t = sq.get_tiles(self.board)
        if not self.grabbed:
            if len(t) == 0:
                _run(stones[self.i - 1] + ascii_lowercase[x] + str(y + 1))
            elif t[-1].color == self.master.players[self.master.player].color:
                self.grabbed = sq
                self.grabbed_first = self.grabbed
                self.grabbed.nridx = self.nridx = 1
                self.render(flip_color(self.master.players[self.master.player].color))
        else:
            x1, y1 = sq.i, sq.j
            x, y = self.grabbed.i, self.grabbed.j
            a, b = abs(x-x1), abs(y-y1)
            if (a <= 1 and b <= 1) and ((a == 1) ^ (b == 1)):
                if a == 0:
                    direction = " -+"[y-y1]
                else:
                    direction = " <>"[x-x1]
                if not self.direction:
                    self.direction = direction
                elif self.direction != direction:
                    return
                x, y = self.grabbed_first.i, self.grabbed_first.j
                self.moves.append(1)
                s = str(self.nridx) + ascii_lowercase[x] + str(y + 1) + direction
                if self.moves:
                    s += ''.join(map(str, self.moves))
                _run(s, f=True)

                if self.grabbed.nridx > 1:
                    self.grabbed.nridx -= 1
                    self.switch_g()
                    self.render(flip_color(self.master.players[self.master.player].color))
            elif a == 0 and b == 0:
                if not self.direction and len(self.grabbed.get_tiles(self.board)) > self.grabbed.nridx:
                    self.grabbed.nridx += 1
                    self.nridx += 1
                else:
                    self.moves[-1] += 1
                self.render(flip_color(self.master.players[self.master.player].color))

    def clear(self, r=True):
        self.grabbed.nridx = self.nridx = 0
        self.i = 1
        self.grabbed = self.grabbed_first = self.direction = False
        self.board = self.master.board
        self.moves = []
        if r:
            self.render(flip_color(self.master.players[self.master.player].color))

    def switch_g(self):
        n = self.grabbed.nridx
        x, y = self.grabbed.get_square(self.board) \
            .next(self.direction, self.size)
        self.grabbed = self.squares[y * self.size + x]
        self.grabbed.nridx = n

    def possibles(self, color):
        if not self.grabbed:
            for sq in self.squares:
                t = sq.get_tiles(self.board)
                if t:
                    yield t[-1].color == color
                else:
                    yield True
        else:
            sq = self.grabbed.get_square(self.board)
            ps = [False] * (self.size ** 2)
            for d in DIRS:
                x, y = sq.next(d, self.size)
                t = self.board.board[x][y].tiles
                if t:
                    ps[y * self.size + x] = t[-1].stone is FLAT
                else:
                    ps[y * self.size + x] = True

            yield from ps

    def execute(self, move, player, old_board):
        new_board = self.board.copy()
        new_board.force_str(move, player)
        idx = 0
        for rn, ro in zip(new_board.board, old_board.board):
            for nsq, sq in zip(rn, ro):
                if str(nsq) != str(sq):
                    self.actives[idx] = True
                idx += 1
        # self.render()
        self.move = move, old_board

    def animate(self, move, old_board):
        print("animating", move)
        m = str_to_move(move)
        sq = int(ascii_lowercase.index(m.col)), int(m.row) - 1
        moves = m.moves if m.moves else [m.total]
        print("found", sq, moves)
        t = m.total
        for i, move in enumerate(moves):
            stop = -(t - move)
            if stop == 0:
                stop = None
            self._animate(sq, m.direction, i, move, old_board, slice(-t, stop))
            t -= move

    def _animate(self, sq, direction, i, n, old_board, idxs):
        print("\t_animating", sq, direction, i, n, idxs)

        vis = self.get_square(sq)
        tiles = vis.get_tiles(old_board)[idxs]
        ids = vis.ids[idxs]

        nvis = Square(*sq).tru_next(direction, self.size)
        for j in range(i):
            nvis = Square(*nvis).tru_next(direction, self.size)
        nts = self.get_square(nvis).get_tiles(old_board)

        step = SQUARE_SIZE / ANIM_STEPS * (i + 1)
        xi, yi = None, None
        if direction == UP:
            step -= (3 * len(nts)) / ANIM_STEPS
            xi, yi = step, 0
        elif direction == DOWN:
            xi, yi = -step, 0
        elif direction == RIGHT:
            xi, yi = 0, -step
        elif direction == LEFT:
            xi, yi = 0, step

        for k in range(2, ANIM_STEPS):
            for _id in ids:
                self.canvas.delete(_id)
            ids = [vis.render_tile(tile, _idx, -(yi * k), (xi * k) - ((_idx - 1) * 3) * (k / ANIM_STEPS))
                   for _idx, tile in enumerate(tiles, start=1)]
            self.update()

    def get_square(self, sq) -> ViewSquare:
        return self.squares[sq[0] * self.size + sq[1]]

    def render(self, color):
        if self.move is not None:
            if str_to_move(self.move[0]).direction is not None:
                self.animate(self.move[0], self.move[1])
        self.canvas.delete("all")

        for s, a, p in zip(self.squares, self.actives, self.possibles(color)):
            s.render(a, p)
        self.canvas.create_line(3, 3, self.winfo_width(), 3, tags="line")
        self.canvas.create_line(3, 3, 3, self.winfo_height(), tags="line")
        self.actives = [False for _ in range(self.size ** 2)]


class _Canvas(tk.Canvas):
    def __init__(self, master, width, height, bd=5, relief=tk.GROOVE):
        self.master = master
        self.board = master.board
        self.players = master.players
        self.width = width
        self.height = height
        self.name1, self.name2 = self.get_name(0), self.get_name(1)

        tk.Canvas.__init__(self, master, bd=bd, relief=relief, width=width, height=height)

    def get_player(self, player):
        return self.players[player]

    def get_name(self, player):
        return self.get_player(player).name.title()

    def calc_stones(self, player):
        p = self.get_player(player)
        return self.master.board.caps - p.caps, self.master.board.stones - p.stones

    def render(self):
        raise NotImplementedError()


class FlatCanvas(_Canvas):
    def __init__(self, master):
        _Canvas.__init__(self, master, master.board.size * SQUARE_SIZE, 30, bd=0)

    def render(self):
        self.delete("all")
        w, b = self.board.count_flats(WHITE), self.board.count_flats(BLACK)
        try:
            s = (w / (w + b)) * self.width
        except ZeroDivisionError:
            s = self.width / 2
        if s != 0:
            self.create_rectangle(0, 0, s, self.height, fill=WHITE, outline=BLACK)
            self.create_text(s/2, self.height / 2, text=w)
        if s != self.width:
            self.create_rectangle(s, 0, self.width, self.height, fill=BLACK)
            self.create_text(s + (self.width-s)/2, self.height / 2, text=b, fill=WHITE)


class TilesCanvas(_Canvas):
    def __init__(self, master):
        self.step = TILE_SIZE / 4
        _Canvas.__init__(self, master,
                         width=TILE_SIZE+len(master.players[0].name)*24,
                         height=self.step*(master.board.stones+master.board.caps) + 125)

    def render(self):
        self.delete("all")

        for player in range(2):
            self.create_text(self.get_x(player), 40, font=("Ubuntu Mono", 24),
                             text="{}\n{}+{}".format(self.get_name(player), *self.calc_stones(player)))
            self.draw_tiles(player)

    def get_x(self, player):
        return [TILE_SIZE, len(self.name1) * 24][player]

    def draw_tiles(self, player):
        p = (player + 1) % 2
        x2, y2 = self.get_x(p) + 20, self.height
        x1, y1 = x2 - TILE_SIZE, y2 - TILE_SIZE
        for i in range(self.calc_stones(p)[1]):
            self.create_rectangle(x1, y1, x2, y2, fill=COLORS[player], outline=COLORS[p])
            y1 -= self.step
            y2 -= self.step
        s = TILE_SIZE / 2
        for i in range(self.calc_stones(p)[0]):
            self.create_circle(x2-s, y2-s, s, fill=COLORS[player], outline=COLORS[p])
            y2 -= self.step
