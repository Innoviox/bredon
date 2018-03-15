from controller import *
#
g = ViewGame(size=5)
# g.run()
ms = zip("a2 d5 a5 a3 d4 a4 Ce4 a4+ b1 a1 Sa4 Cb4 a4+ b4< e3 b4 b1< a2- e1 Se2 b3 b4- d3 a4+ Sc5 a4 Sa2 b2 a2+ 2a5- b4 2a4> 2a3+11 b5 3a5> b1 Sa5 1b4+ 2b4-11 a3 a2 2a1+ 2b2< 2a4-11 2b3< 2a2+ b3< 4a2+ Sa2 4b5-211 a2+ b2+ c2 1b3< b2 3a3> a5> 4a3- Sa5 2b3+11 2b4- 3a3> b2< 1a3- c3 4b3+".split(),
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
          WHITE, BLACK
          ))

for i, (m, c) in enumerate(ms):
    # print(m, c)
    g.vboard.execute(m, c, g.board.copy())
    g.board.execute(str_to_move(m), c)
    g.viz()
    # print(g.board)
    time.sleep(1)