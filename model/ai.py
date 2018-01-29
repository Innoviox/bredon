from .board import Board, cols, tile_to_coords, coords_to_tile, EMPTY, dirs

class StaticMoveAI(object):
    def __init__(self, board):
        self.board = board

    def generate_all_moves(self):
        for y in range(self.board.h):
            for x in range(self.board.w):
                if self.board.board[y][x] == EMPTY:
                    yield coords_to_tile(y, x)
                else:
                    for dir in dirs:
                        yield # TODO: Generate move strings


    def pick_move(self):
        ...
