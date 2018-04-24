from .notation import *
from .ai       import *

def load_moves_from_file(filename, out=False):
    with open(filename) as file:
        ptn = file.read()
        _, s = ptn.split("Size")
        ptn = s.split("\n")
        size = int(s[2])
        b = Board(size)
        curr_player = WHITE
        for iturn, turn in enumerate(ptn[2:]):
            if 'R' in turn:
                break
            for imove, move in enumerate(turn.split(" ")[1:]):  # Exclude the round number
                if move:
                    if iturn == 0:
                        curr_player = [BLACK, WHITE][imove]
                    elif iturn == 1 and imove == 0:
                        curr_player = WHITE

                    b.force(b.parse_move(str_to_move(move), curr_player))

                    if out:
                        print(move)
                        print(str_to_move(move))
                        print(b)
                        print("Road?:", b.road())

                    if curr_player == BLACK:
                        curr_player = WHITE
                    else:
                        curr_player = BLACK

                    yield b, move
    return b
