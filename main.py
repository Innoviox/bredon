from model import *

# board = load_moves_from_file("games/sarras vs takkybot 18.1.27 14.15.ptn")
# print(board)
board = Board(4, 4)  # load_moves_from_file("You vs You 18.1.29 20.43.ptn")
board.force(board.parse_move(Move(col='a', row=3), BLACK))
board.force(board.parse_move(Move(col='c', row=3), WHITE))
'''
board.force_str("c2", WHITE)
board.force_str("c1", WHITE)
print(board)
print(board.road())
'''
# new_board = board.copy()
# new_board.force_str("e4", WHITE)
# print(new_board)
# print(new_board.evaluate(WHITE))
# input()
ai = MinimaxAI(board, WHITE, depth=2)
ai2 = MinimaxAI(board, BLACK, depth=2)
# p = Player(board, BLACK)
ptn = ""
i = 1
while not board.winner([ai, ai2]):
    ptn += str(i) + ". "
    ai_move = ai.pick_move()
    print(ai_move)
    ai.do(ai_move)
    print(board)
    ptn += ai_move.to_ptn() + " "
    # input(board._road())

    ai_move = ai2.pick_move()
    print(ai_move)
    ai2.do(ai_move)
    print(board)
    ptn += ai_move.to_ptn()

    ptn += "\n"
    i += 1
    # input(board._road())
print(board.winner([ai, ai2]))
    #
    # # board.force(board.parse_move(ai_move, ai.curr_player))
    # # ai.switch_player()
    # print(board)
    # # my_move = board.parse_move()
    # # while not board.valid(my_move):
    # #     my_move = board.parse_move(input("Enter move: "), BLACK)
    # while 1:
    #     try:
    #         p.do(str_to_move(input("Enter move: ")))
    #         break
    #     except Exception as e:
    #         print("Error:", e)
    # print(board)
