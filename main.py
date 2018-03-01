from controller import *

input()
g = Game(size=4, white_type=(AI, 3)) # black_type=HUMAN)
g.run()

'''
moves = zip("a1 a2 a3 b3 Sa4".split(),
             (WHITE, WHITE, WHITE, WHITE, BLACK))
for m, c in moves:
    g.board.force_str(m, c)
print(g.board)
m = g.player_2.pick_move()
print(m)
g.player_2.do(m)
print(g.board)
'''