from .notation import *
from .player   import *

def load_moves_from_file(filename, out=False):
    with open(filename) as file:
        ptn_str = file.read()
        _, s = ptn_str.split("Size")
        ptn_str = s.split("\n")
        size = int(s[2])
        b = Board(size)
        curr_player = Colors.WHITE
        ptn = PTN()
        for iturn, turn in enumerate(ptn_str[2:]):
            if 'R' in turn:
                break
            for imove, move in enumerate(turn.split(" ")[1:]):  # Exclude the round number
                if move:
                    if iturn == 0:
                        curr_player = [Colors.BLACK, Colors.WHITE][imove]
                    elif iturn == 1 and imove == 0:
                        curr_player = Colors.WHITE

                    b.force(b.parse_move(str_to_move(move), curr_player))

                    if out:
                        print(move)
                        print(str_to_move(move))
                        print(b)
                        print("Road?:", b.road())

                    if curr_player == Colors.BLACK:
                        curr_player = Colors.WHITE
                    else:
                        curr_player = Colors.BLACK
                    ptn.append(move)
                    yield b, move
    yield b, ptn
