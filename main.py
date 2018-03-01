from controller import *

input()
g = Game(size=4, white_type=(AI, 3)) # black_type=HUMAN)
# g.run()


moves = zip("d4 a1 b2 d2 a2 c4 a3 a4 b4 1c4< 1a3+ 2b4< 1a1> c4 Sb4 Sa1 c2 d3 Sd1 c3 1b4< c1 1b1> 1a1> a1 1b1+ b1 2b2> b2 3c2< c2 4b2> b2 Sb4 1a2- a2 a3 1a2- 1d1+ 3a1> b3 4b1>".split(),
             (BLACK, WHITE,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK, WHITE, BLACK,
              WHITE, BLACK, WHITE, BLACK)
)
for i, (m, c) in enumerate(moves):
    # g.board.force_str(m, c)
    g.players[i % 2]._do(str_to_move(m), c)
    print(g.board)
    for player in g.players:
        print(player.color, player.out_of_tiles(), player.caps, player.stones, g.board.caps, g.board.stones)
# m = g.player_2.pick_move()
# print(m)
# g.player_2.do(m)
# print(g.board)
