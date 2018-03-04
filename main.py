from controller import *

input()
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
moves = zip("Sc2 c1 c1+".split(),
             (BLACK, WHITE,
              WHITE)
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
m = g.player_2.pick_move(out=True)
print(m)
g.player_2.do(m)
print(g.board)
'''