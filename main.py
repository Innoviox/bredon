from controller import *

input()
g = Game(size=4, white_type=(AI, 3), black_type=(AI, 3)) # black_type=HUMAN)
g.run()

'''
moves = zip("a1 d4 d2 b2 c3 a2 b3".split(),
             (BLACK, WHITE,
              WHITE, BLACK, WHITE, BLACK, WHITE)
)
for i, (m, c) in enumerate(moves):
    # g.board.force_str(m, c)
    g.players[i % 2]._do(str_to_move(m), c)
    print(g.board)
    for player in g.players:
        print(player.color, player.out_of_tiles(), player.caps, player.stones, g.board.caps, g.board.stones)
# print(g.player_1.do(str_to_move("3c3-111")))
# print(g.board)
m = g.player_2.pick_move(out=True)
print(m)
g.player_2.do(m)
print(g.board)
'''