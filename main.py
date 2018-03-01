from controller import *

input()
g = Game(size=4) # black_type=HUMAN)
g.run()

# moves = zip("a1 e5 a2 Cd4 a3 e4 a4".split(),
#             (WHITE, BLACK, WHITE, BLACK, WHITE, BLACK, WHITE, BLACK))
# for m, c in moves:
#     g.board.force_str(m, c)
# print(g.board)
# m = g.player_2.pick_move()
# print(m)
# g.player_2.do(m)
# print(g.board)