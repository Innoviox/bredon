from controller import *

input()
g = Game(size=5, white_type=(AI, 5), black_type=(AI, 5)) # black_type=HUMAN)
g.run()

'''
moves = zip("d4 a1 d3 Sd2 1d3+ d3 2d4- 1d2+ Sd4 4d3<211 1b3> d3 ".split(),
             (BLACK, WHITE,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK)
)
for i, (m, c) in enumerate(moves):
    # g.board.force_str(m, c)
    g.players[i % 2]._do(str_to_move(m), c)
    print(g.board)
    for player in g.players:
        print(player.color, player.out_of_tiles(), player.caps, player.stones, g.board.caps, g.board.stones)
print(g.player_1.do(str_to_move("3c3-111")))
print(g.board)
# m = g.player_2.pick_move()
# print(m)
# g.player_2.do(m)
# print(g.board)
'''