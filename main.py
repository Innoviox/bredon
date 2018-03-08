from controller import *

# for b in load_moves_from_file("/Users/chervjay/Documents/GitHub/Bredon/neural/games/6.ptn"):
#     print(b)
# input()
g = Game(size=5, white_type=(AI, 3), black_type=(AI, 3)) # black_type=HUMAN)
g.run()

# 1. a1 e5
# 2. Ce3 Cb2
# 3. d4 Sa2
# 4. c4 a3
# 5. e4 Sc2
# 6. a4 Sb4
# 7. d5 1a1>
# 8. b5 1b4>
# 9. d2 c3
# 10. c5 2c4+
# 11. 1b5> Sb5
# 12. b3 1a3>
# 13. 3c5<12

'''
moves = zip("a1 d4 d3 a2 c3 b2 d2 d1 b4 a3 Sa4 1a1> c1 1b1> 1d2- 2c1> c4 4d1<13 d1 d2 1d3- 1c1> 2d2- d3 Sa1 1a2> b3 c2 c1 1d3+ 4d1+121 1c2- 1a1> 1b2+ 3b1+12 2c1< 3b3-12 a2 c2 3b2> 1d2< 2d3<11 4c2<22 ".split(),
             (BLACK, WHITE,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,
              WHITE, BLACK,)
)
for i, (m, c) in enumerate(moves):
    # g.board.force_str(m, c)
    print(m, c, g.board.valid_move(str_to_move(m), c))
    g.players[i % 2]._do(str_to_move(m), c)
    print(g.board)
    for player in g.players:
        print(player.color, player.out_of_tiles(), player.caps, player.stones, g.board.caps, g.board.stones)
# print(g.player_1.do(str_to_move("3c3-111")))
# print(g.board)
# m = g.player_1.pick_move(out=True)
# print(m)
# g.player_1.do(m)
# print(g.board)
'''